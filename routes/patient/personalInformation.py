from flask import Blueprint
from controllers.patient.personalInformation import PersonalInformation

patient_personal_info_route = Blueprint('patient', __name__)

@patient_personal_info_route.route('/patient/personal_info/account_id=<int:account_id>', methods=['GET'])
def get_patient_by_id(account_id):
    return PersonalInformation.get_by_id(account_id)