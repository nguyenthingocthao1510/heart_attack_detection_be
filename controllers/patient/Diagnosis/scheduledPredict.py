import pickle, threading, time, schedule
from copy import deepcopy
from flask import request, jsonify
import pandas as pd
from controllers.patient.Diagnosis.preprocess import DataPreprocessor
from utils.logger import Logger

class ScheduledDiagnosis:
    def __init__(self):
        with open(r'controllers/patient/Diagnosis/svc.pkl', 'rb') as model_file:
            self.svc = pickle.load(model_file)
        with open(r'controllers/patient/Diagnosis/scaler.pkl', 'rb') as scaler_file:
            self.scaler = pickle.load(scaler_file)
        
        self.temp_storage = {
            'sensor_input': None,
            'user_input': None
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

        self.logger = Logger("ManualDiagnosis")

    def receive_sensor_data(self):
        if request.method == 'POST':
            self.logger.info("Waiting sensor to retrieve data...")

            data=request.get_json()

            self.logger.debug(f"Raw sensor data received: {data}")

            with self.storage_lock:
                self.temp_storage['sensor_input'] = data
                self.check_data_ready()

            return jsonify({
                'message': 'successfully received sensor data',
                'data': data
            }), 200
        
    def schedule_predict(self):
        self.logger.info("Start scheduled prediction...")
        with self.storage_lock:
            sensor_input = self.temp_storage['sensor_input']
            user_input = self.temp_storage['user_input']

        if not sensor_input or not user_input:
            print("Incomplete data for periodic prediction.")
            return

        combined_data = {**sensor_input, **user_input}
        copied_data = deepcopy(combined_data)

        combined_data = self.preprocessor.preprocess(combined_data)
        combined_data['restecg'] = self.preprocessor.encode_restecg(combined_data['restecg'])

        self.logger.debug(f"Combined data after preprocessing: {combined_data}")

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

        return jsonify({
            'result': result
        }), 200
    
    def run_scheduler(self):
        schedule.every(5).minutes.do(self.schedule_predict)
        while True:
            schedule.run_pending()
            time.sleep(1)

