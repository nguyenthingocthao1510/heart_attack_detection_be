from flask import Blueprint
from controllers.doctor.patient import get_all, get_by_id, add, update, delete, get_for_list

patient_route = Blueprint('patient', __name__)

@patient_route.route('/doctor/patients', methods=['GET'])
def get_all_patient():
    return get_all()

@patient_route.route('/doctor/patient/id=<int:id>', methods=['GET'])
def get_patient_by_id(id):
    return get_by_id(id)

@patient_route.route('/doctor/list-patients', methods = ['POST'])
def filter_patients():
    return get_for_list()

@patient_route.route('/doctor/add', methods = ['POST'])
def add_patient():
    return add()

@patient_route.route('/doctor/update/id=<int:id>', methods=['PUT'])
def update_patient(id):
    return update(id)

@patient_route.route('/doctor/delete/id=<int:id>', methods=['DELETE'])
def delete_patient(id):
    return delete(id)

