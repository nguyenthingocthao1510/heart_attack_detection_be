from flask import Blueprint
from controllers.patient.profile.profile import ProfileRepo

profile = ProfileRepo()
patient_profile_route = Blueprint('patient', __name__)

@patient_profile_route.route('/patient/personal_info/account_id=<int:account_id>', methods=['GET'])
def get_patient_by_id(account_id):
    return profile.get_by_id(account_id)

@patient_profile_route.route('/patient/update-need-prediction', methods=['PUT'])
def update_need_prediction():
    return profile.update_need_prediction()