from flask import Blueprint
from controllers.category.Doctor.doctor import get_all, get_by_id, create, update, delete, get_for_list

doctor_route = Blueprint('doctor_route', __name__)
@doctor_route.route('/doctors', methods = ['GET'])
def get_all_doctor():
    return get_all()

@doctor_route.route('/doctor/accountId=<int:account_id>', methods = ['GET'])
def get_doctor_by_id(account_id):
    return get_by_id(account_id)

@doctor_route.route('/doctor/list-doctors', methods = ['POST'])
def filter_doctor():
    return get_for_list()

@doctor_route.route('/doctor/create-information', methods = ['POST'])
def add_doctor():
    return create()

@doctor_route.route('/doctor/update-information/doctorId=<int:id>', methods = ['PUT'])
def update_doctor(id):
    return update(id)

@doctor_route.route('/doctor/delete-information/doctorId=<int:id>', methods = ['DELETE'])
def delete_doctor(id):
    return delete(id)