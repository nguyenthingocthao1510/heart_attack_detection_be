import pickle
import threading
from copy import deepcopy
from flask import request, jsonify
import pandas as pd
from controllers.patient.Diagnosis.preprocess import DataPreprocessor

class DiagnosisService:
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

    def receive_sensor_data(self):
        if request.method == 'POST':
            data=request.get_json()
            data['restecg'] = self.preprocessor.encode_restecg(int(data['restecg']))

            with self.storage_lock:
                self.temp_storage['sensor_input'] = data
                self.check_data_ready()

            return jsonify({
                'message': 'successfully received sensor data',
                'data': data
            }), 200
        
    def receive_user_data(self):
        if request.method == 'POST':
            data = request.get_json()
            data = self.preprocessor.preprocess(data)
            
            with self.storage_lock:
                self.temp_storage['user_input'] = data
                self.check_data_ready()

            return jsonify({
                'message': 'successfully received user data',
                'data': data
            }), 200
    
    def check_data_ready(self):
        if self.temp_storage['sensor_input'] and self.temp_storage['user_input']:
            self.data_ready.set()

    def predict(self):

        self.data_ready.wait()

        with self.storage_lock:
            sensor_input = self.temp_storage['sensor_input']
            user_input = self.temp_storage['user_input']

        if not sensor_input or not user_input:
            return jsonify({'error': 'Missing data. Ensure both sensor and user inputs are provided.'}), 400

        combined_data = {**sensor_input, **user_input}
        saved_data = deepcopy(combined_data)

        df = pd.DataFrame([combined_data])

        df = pd.get_dummies(df, columns=['sex', 'exng', 'caa', 'cp', 'fbs', 'restecg', 'slp', 'thall'])

        df = df.reindex(columns=self.model_cols, fill_value=0)

        con_cols = ['age', 'trtbps', 'chol', 'thalachh', 'oldpeak']
        df[con_cols] = self.scaler.transform(df[con_cols])

        prediction = self.svc.predict(df)

        return jsonify({
            'prediction': int(prediction[0]),
            'diagnosis': saved_data
        }), 200
