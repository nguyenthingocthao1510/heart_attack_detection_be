from flask import Blueprint, Flask
from controllers.patient.Diagnosis.Prediction.manualPredict import ManualDiagnosis
from controllers.patient.Diagnosis.Prediction.scheduledPredict import ScheduledDiagnosis

diagnosis_route = Blueprint('diagnosis', __name__)

manual_diagnosis = ManualDiagnosis()
scheduled_diagnosis = ScheduledDiagnosis()

app = Flask(__name__)

@diagnosis_route.route('/patient/manual/diagnosis', methods=['POST'])
def manual_diagnose():
    return manual_diagnosis.manual_predict()

@diagnosis_route.route('/patient/manual/receive-sensor-data', methods=['POST'])
def receive_sensor_data():
    return manual_diagnosis.receive_sensor_data()

@diagnosis_route.route('/patient/manual/receive-user-data', methods=['POST'])
def receive_user_data():
    return manual_diagnosis.receive_user_data()

@diagnosis_route.route('/patient/scheduled/diagnosis', methods=['POST'])
def scheduled_diagnose():
    return scheduled_diagnosis.scheduled_predict()

@diagnosis_route.route('/patient/scheduled/receive-sensor-data', methods=['POST'])
def receive_sensor_data_scheduled():
    return scheduled_diagnosis.receive_sensor_data()

@diagnosis_route.route('/patient/scheduled/receive-user-data', methods=['POST'])
def receive_user_data_scheduled():
    return scheduled_diagnosis.receive_user_data()