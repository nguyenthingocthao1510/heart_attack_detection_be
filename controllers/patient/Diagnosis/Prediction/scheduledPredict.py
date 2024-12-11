import pickle, threading, time, schedule
from copy import deepcopy
from flask import request, jsonify
import pandas as pd
from controllers.patient.Diagnosis.Prediction.preprocess import DataPreprocessor
from utils.logger import Logger

class ScheduledDiagnosis:
    def __init__(self):
        with open(r'controllers/patient/Diagnosis/pickle/lr.pkl', 'rb') as model_file:
            self.svc = pickle.load(model_file)
        with open(r'controllers/patient/Diagnosis/pickle/scaler.pkl', 'rb') as scaler_file:
            self.scaler = pickle.load(scaler_file)
        
        self.temp_storage = {
            'sensor_input': {},
            'user_input': {}
        }

        self.storage_lock = threading.Lock()
        self.data_ready = threading.Event()

        self.model_cols = [
            'age', 'trtbps', 'chol', 'thalachh', 'oldpeak',
            'sex_1', 'exng_1', 'caa_1', 'caa_2', 'caa_3', 'caa_4',
            'cp_1', 'cp_2', 'cp_3', 'fbs_1', 
            'restecg_1', 'restecg_2', 'slp_1', 'slp_2',
            'thall_1', 'thall_2', 'thall_3'
        ]

        self.preprocessor = DataPreprocessor()

        self.logger = Logger("ScheduledPrediction")

    def receive_sensor_data(self):
        if request.method == 'POST':
            self.logger.info(f"Sensor data received at {time.strftime('%Y-%m-%d %H:%M:%S')}")
            data=request.get_json()

            with self.storage_lock:
                self.temp_storage['sensor_input'] = data
                self.check_data_ready()

        return data
        
    def receive_user_data(self):
        if request.method == 'POST':
            self.logger.info(f"User data received at {time.strftime('%Y-%m-%d %H:%M:%S')}")
            data = request.get_json()
            
            with self.storage_lock:
                self.temp_storage['user_input'] = data
                self.check_data_ready()

        return data
    
    def check_data_ready(self):
        if self.temp_storage['sensor_input'] and self.temp_storage['user_input']:
            self.logger.debug("Data ready: Both sensor and user data received.")
            self.data_ready.set()

        
    def scheduled_predict(self):
        self.logger.info("Scheduler triggered prediction...")

        self.logger.debug(f"User data in temp storage: {self.temp_storage['user_input']}")
        self.logger.debug(f"Sensor data in temp storage: {self.temp_storage['sensor_input']}")

        if not self.data_ready.wait(timeout=30):
            self.logger.warning("No data received within the timeout.")
            return

        with self.storage_lock:
            sensor_input = deepcopy(self.temp_storage.get('sensor_input'))
            user_input = deepcopy(self.temp_storage.get('user_input'))
            self.temp_storage['sensor_input'] = None
            self.temp_storage['user_input'] = None
            self.data_ready.clear()

        self.logger.debug(f"Sensor data: {sensor_input}")
        self.logger.debug(f"User data: {user_input}")

        if not sensor_input or not user_input:
            self.logger.warning("Incomplete data for prediction.")
            return

        combined_data = {**sensor_input, **user_input}
        copied_data = deepcopy(combined_data)

        combined_data = self.preprocessor.preprocess(combined_data)
        combined_data['restecg'] = self.preprocessor.encode_restecg(int(combined_data['restecg']))

        df = pd.DataFrame([combined_data])

        df = pd.get_dummies(df, columns=['sex', 'exng', 'caa', 'cp', 'fbs', 'restecg', 'slp', 'thall'])

        df = df.reindex(columns=self.model_cols, fill_value=0)

        con_cols = ['age', 'trtbps', 'chol', 'thalachh', 'oldpeak']
        df[con_cols] = self.scaler.transform(df[con_cols])

        prediction = self.svc.predict(df)

        result = {
            'prediction': int(prediction[0]),
            'thalachh': copied_data['thalachh'],
            'restecg': copied_data['restecg'],
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }

        self.logger.debug(f"Scheduled prediction result: {result}")
        return result

    
    def run_scheduler(self):
        self.logger.info("Starting scheduler after a brief delay...")
        time.sleep(15)
        self.logger.info("scheduler started...")
        schedule.every(15).seconds.do(self.scheduled_predict)

        while True:
            try:
                schedule.run_pending()
                time.sleep(1)
            except Exception as e:
                self.logger.error(f"Scheduler encountered an error: {e}")
                self.logger.info("Restarting scheduler...")

