from flask import Blueprint, Flask
from controllers.patient.diagnosis.prediction.manualPredict import ManualDiagnosis
from controllers.patient.diagnosis.prediction.scheduledPredict import ScheduledDiagnosis
from controllers.patient.diagnosis.diagnosisHistory.diagnosisHistory import DiagnosisHistoryRepo
from controllers.patient.profile import ProfileController
from controllers.patient.patientRecord.patientRecord import get_record_by_patient_id
from controllers.patient.sensor.sensor import SensorRepo

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
dh_repo = DiagnosisHistoryRepo()
profile = ProfileController()
sensor_repo = SensorRepo()

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

@diagnosis_route.route('/sensor/add-history-by-patient-id', methods=['POST'])
def add_history_by_patient_id(patient_id, thalachh, restecg):
    return dh_repo.add_by_patient_id(patient_id, thalachh, restecg)