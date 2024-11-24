from flask import Blueprint
from controllers.patient.Diagnosis.predict import HeartAttackPredictor

diagnosis_route = Blueprint('diagnosis', __name__)

predictor = HeartAttackPredictor()

@diagnosis_route.route('/patient/diagnosis', methods=['POST'])
def diagnose_heart_attack():
    return predictor.predict()