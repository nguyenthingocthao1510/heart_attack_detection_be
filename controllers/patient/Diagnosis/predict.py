import pickle
from copy import deepcopy
from flask import request, jsonify
import pandas as pd
from controllers.patient.Diagnosis.preprocess import DataPreprocessor

class HeartAttackPredictor:
    def __init__(self):
        with open(r'controllers/patient/Diagnosis/svc.pkl', 'rb') as model_file:
            self.svc = pickle.load(model_file)
        with open(r'controllers/patient/Diagnosis/scaler.pkl', 'rb') as scaler_file:
            self.scaler = pickle.load(scaler_file)
        
        self.model_cols = [
            'age', 'trtbps', 'chol', 'thalachh', 'oldpeak',
            'sex_1', 'exng_1', 'caa_1', 'caa_2', 'caa_3', 'caa_4',
            'cp_1', 'cp_2', 'cp_3', 'fbs_1', 
            'restecg_1', 'restecg_2', 'slp_1', 'slp_2',
            'thall_1', 'thall_2', 'thall_3'
        ]
        self.preprocessor = DataPreprocessor()

    def predict(self):
        data = request.get_json()

        saved_data = deepcopy(data)

        data = self.preprocessor.preprocess(data)

        required_keys = [
            'age', 'trtbps', 'chol', 'thalachh', 'oldpeak', 
            'sex', 'exng', 'caa', 'cp', 'fbs', 'restecg', 'slp', 'thall'
        ]
        if not data or not all(key in data for key in required_keys):
            return jsonify({'error': 'Missing value, please enter again.'}), 400

        df = pd.DataFrame([data])

        df = pd.get_dummies(df, columns=['sex', 'exng', 'caa', 'cp', 'fbs', 'restecg', 'slp', 'thall'])

        df = df.reindex(columns=self.model_cols, fill_value=0)

        con_cols = ['age', 'trtbps', 'chol', 'thalachh', 'oldpeak']
        df[con_cols] = self.scaler.transform(df[con_cols])

        prediction = self.svc.predict(df)

        return jsonify({
            'prediction': int(prediction[0]),
            'diagnosis': saved_data
        }), 200
