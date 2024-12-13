import pickle, time
from copy import deepcopy
import pandas as pd
from utils.logger import Logger
from controllers.patient.Diagnosis.Prediction.preprocess import DataPreprocessor

class BasePredictor:
    def __init__(self, model_path, scaler_path, logger_name):
        with open(model_path, 'rb') as model_file:
            self.model = pickle.load(model_file)
        with open(scaler_path, 'rb') as scaler_file:
            self.scaler = pickle.load(scaler_file)

        self.preprocessor = DataPreprocessor()
        self.logger = Logger(logger_name)

        self.model_cols = [
            'age', 'trtbps', 'chol', 'thalachh', 'oldpeak',
            'sex_1', 'exng_1', 'caa_1', 'caa_2', 'caa_3', 'caa_4',
            'cp_1', 'cp_2', 'cp_3', 'fbs_1', 
            'restecg_1', 'restecg_2', 'slp_1', 'slp_2',
            'thall_1', 'thall_2', 'thall_3'
        ]

    def predict(self, sensor_input, user_input):
        self.logger.info("Processing and predicting...")

        combined_data = {**sensor_input, **user_input}
        saved_data = deepcopy(combined_data)

        combined_data = self.preprocessor.preprocess(combined_data)
        combined_data['restecg'] = self.preprocessor.encode_restecg(int(combined_data['restecg']))

        df = pd.DataFrame([combined_data])
        df = pd.get_dummies(df, columns=['sex', 'exng', 'caa', 'cp', 'fbs', 'restecg', 'slp', 'thall'])
        df = df.reindex(columns=self.model_cols, fill_value=0)

        con_cols = ['age', 'trtbps', 'chol', 'thalachh', 'oldpeak']
        df[con_cols] = self.scaler.transform(df[con_cols])

        prediction = self.model.predict(df)

        return {
            'prediction': int(prediction[0]),
            'thalachh': saved_data['thalachh'],
            'restecg': saved_data['restecg'],
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }

