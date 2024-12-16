from flask import Blueprint
from controllers.patient.profile import ProfileController

patient_profile_route = Blueprint('patient', __name__)

@patient_profile_route.route('/patient/personal_info/account_id=<int:account_id>', methods=['GET'])
def get_patient_by_id(account_id):
    return ProfileController.get_by_id(account_id)