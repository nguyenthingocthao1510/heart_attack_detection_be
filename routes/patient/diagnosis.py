from flask import Blueprint, Flask
from controllers.patient.Diagnosis.Prediction.manualPredict import ManualDiagnosis
from controllers.patient.Diagnosis.Prediction.scheduledPredict import ScheduledDiagnosis

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
    return scheduled.receive_sensor_data()

@diagnosis_route.route('/patient/scheduled/receive-user-data', methods=['GET'])
def receive_user_data_scheduled():
    return scheduled.receive_user_data()