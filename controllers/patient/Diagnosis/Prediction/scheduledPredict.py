import time, schedule
from config.dbconfig.app import db
from controllers.patient.Diagnosis.Prediction.basePredict import BasePredictor
from controllers.patient.patientRecord.patientRecord import get_record_by_patient_id
from controllers.patient.sensor.sensor import SensorRepo
from controllers.patient.Diagnosis.diagnosisHistory.diagnosisHistory import DiagnosisHistoryRepo

class ScheduledDiagnosis(BasePredictor):
    def __init__(self):
        super().__init__(
            model_path=r'controllers/patient/Diagnosis/Prediction/pickle/lr.pkl',
            scaler_path=r'controllers/patient/Diagnosis/Prediction/pickle/scaler.pkl',
        )

        self.dh_repo = DiagnosisHistoryRepo()
        self.sensor_repo = SensorRepo()
    
    def combine_data(self, sensor_input, user_input):
        lookup = {id['patient_id']: id for id in user_input}

        combined_data = []
        for id in sensor_input:
            pid = id['patient_id']
            if pid in lookup:
                merged = {**id, **lookup[pid]}
                combined_data.append(merged)

        self.logger.debug(f'Combined data: {combined_data}')
        return combined_data

    def predict(self):
        sensor_input = self.sensor_repo.receive_sensor_data()
        user_input = get_record_by_patient_id()
        combined_data = self.combine_data(sensor_input, user_input)

        result_list = []
        for cd in combined_data:
            result = super().predict(cd)
            result_list.append(result)

            self.dh_repo.add_by_patient_id(cd['patient_id'], result['prediction'], result['thalachh'], result['restecg'], result['timestamp'])

        self.logger.debug(f'Result list: {result_list}')
        return result_list
    
    def run_scheduler(self):
        self.logger.info("Starting scheduler after a brief delay...")
        time.sleep(5)
        self.logger.info("scheduler started...")
        schedule.every(4).weeks.do(self.predict)

        while True:
            try:
                schedule.run_pending()
                time.sleep(1)
            except Exception as e:
                self.logger.error(f"Scheduler encountered an error: {e}")
                self.logger.info("Restarting scheduler...")

