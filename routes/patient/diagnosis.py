from flask import Blueprint, Flask
from controllers.patient.Diagnosis.predict import DiagnosisService

diagnosis_route = Blueprint('diagnosis', __name__)

diagnosis_service = DiagnosisService()

app = Flask(__name__)

@diagnosis_route.route('/patient/diagnosis', methods=['POST'])
def diagnose_heart_attack():
    return diagnosis_service.predict()

@diagnosis_route.route('/patient/receive-sensor-data', methods=['POST'])
def receive_sensor_data():
    return diagnosis_service.receive_sensor_data()

@diagnosis_route.route('/patient/receive-user-data', methods=['POST'])
def receive_user_data():
    return diagnosis_service.receive_user_data()