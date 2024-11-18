from flask import Blueprint
from controllers.patient.personalInformation import PatientPersonalInformationController

patient_personal_info_route = Blueprint('patient', __name__)

@patient_personal_info_route.route('/patient/personal_info/id=<int:patient_id>', methods=['GET'])
def get_patient_by_id(id):
    return PatientPersonalInformationController.get_by_id(id)