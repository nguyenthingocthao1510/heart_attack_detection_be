from flask import Blueprint, Flask
from controllers.patient.diagnosis.prediction.manualPredict import ManualDiagnosis
from controllers.patient.diagnosis.prediction.scheduledPredict import ScheduledDiagnosis
from controllers.patient.patientRecord.patientRecord import get_record_by_patient_id
from controllers.patient.sensor.sensor import SensorRepo
from controllers.patient.diagnosis.diagnosisHistory.diagnosisHistory import DiagnosisHistoryRepo

diagnosis_route = Blueprint('diagnosis', __name__)
app = Flask(__name__)

class DiagnosisFactory:
    @staticmethod
    def create_diagnosis(type):
        if type == 'manual':
            return ManualDiagnosis()
        elif type == 'scheduled':
            return ScheduledDiagnosis()
        else:
            raise ValueError(f"Unknown predictor type: {type}")

manual = DiagnosisFactory.create_diagnosis('manual')
scheduled = DiagnosisFactory.create_diagnosis('scheduled')
sensor_repo = SensorRepo()
dh_repo = DiagnosisHistoryRepo()

@diagnosis_route.route('/patient/manual/diagnosis', methods=['POST'])
def manual_diagnose():
    return manual.predict()

@diagnosis_route.route('/patient/manual/receive-sensor-data', methods=['POST'])
def receive_sensor_data():
    return manual.receive_sensor_data()

@diagnosis_route.route('/patient/manual/receive-user-data', methods=['POST'])
def receive_user_data():
    return manual.receive_user_data()

@diagnosis_route.route('/patient/scheduled/diagnosis', methods=['POST'])
def scheduled_diagnose():
    return scheduled.predict()

@diagnosis_route.route('/patient/scheduled/receive-sensor-data', methods=['GET'])
def receive_sensor_data_scheduled():
    return sensor_repo.receive_sensor_data()

@diagnosis_route.route('/patient/scheduled/receive-user-data', methods=['GET'])
def receive_user_data_scheduled():
    return get_record_by_patient_id()

@diagnosis_route.route('/patient/add-diagnosis-history', methods=['POST'])
def add_diagnosis_history():
    return dh_repo.save_diagnosis_history()

@diagnosis_route.route('/patient/get-history/patient_id=<int:patient_id>', methods=['GET'])
def get_history(patient_id):
    return dh_repo.get_history(patient_id)