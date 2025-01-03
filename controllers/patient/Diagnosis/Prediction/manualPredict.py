import threading
from flask import request, jsonify
from controllers.patient.Diagnosis.Prediction.basePredict import BasePredictor
from controllers.patient.Diagnosis.diagnosisHistory.diagnosisHistory import DiagnosisHistoryRepo

class ManualDiagnosis(BasePredictor):
    def __init__(self):
        super().__init__(
            model_path=r'controllers/patient/Diagnosis/Prediction/pickle/lr.pkl',
            scaler_path=r'controllers/patient/Diagnosis/Prediction/pickle/scaler.pkl',
        )

        self.temp_storage = {
            'sensor_input': None,
            'user_input': None
        }
        
        self.dh_repo = DiagnosisHistoryRepo()
        self.storage_lock = threading.Lock()
        self.data_ready = threading.Event()

    def receive_sensor_data(self):
        if request.method == 'POST':
            data = request.get_json()

            with self.storage_lock:
                self.temp_storage['sensor_input'] = data
                self.check_data_ready()

            return jsonify({'message': 'Successfully received sensor data', 'data': data}), 200


    def receive_user_data(self):
        if request.method == 'POST':
            data = request.get_json()

            with self.storage_lock:
                self.temp_storage['user_input'] = data
                self.check_data_ready()

            return jsonify({'message': 'Successfully received user data', 'data': data}), 200


    def check_data_ready(self):
        if self.temp_storage.get('sensor_input') and self.temp_storage.get('user_input'):
            self.data_ready.set()


    def combine_data(self, sensor_input, user_input):
        combined_data = {**sensor_input, **user_input}
        return combined_data

    def predict(self):
        self.data_ready.wait(timeout=10)
        with self.storage_lock:
            if not self.temp_storage['sensor_input'] or not self.temp_storage['user_input']:
                self.temp_storage['sensor_input'] = None
                self.temp_storage['user_input'] = None
                return jsonify({'error': 'Missing sensor or user input data. Please provide both.'}), 400
        
        with self.storage_lock:
            sensor_input = self.temp_storage.get('sensor_input')
            user_input = self.temp_storage.get('user_input')

        if not sensor_input or not user_input:
            return jsonify({'error': 'Timed out waiting for inputs. Please try again.'}), 408
        
        combined_data = self.combine_data(sensor_input, user_input)
        result = super().predict(combined_data)
        with self.storage_lock:
            self.temp_storage['sensor_input'] = None
            self.temp_storage['user_input'] = None


        return jsonify(result), 200

