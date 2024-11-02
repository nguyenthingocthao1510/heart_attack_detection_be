from flask import Blueprint
from controllers.patient.DiagnoseHeartAttack.diagnosis import predict

diagnosis_route = Blueprint('diagnosis', __name__)

@diagnosis_route.route('/patient/diagnosis', methods=['POST'])
def diagnose_heart_attack():
    return predict()