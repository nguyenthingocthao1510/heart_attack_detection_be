from flask import Blueprint
from controllers.patient.healthInsurance.healthInsurance import get_all, get_by_id, insert, update, get_patient_by_id, delete
health_insurance_route = Blueprint('health_insurance_route', __name__)

@health_insurance_route.route('/health-insurances/accountId=<int:account_id>', methods = ['GET'])
def get_all_health_insurance(account_id):
    return get_all(account_id)

@health_insurance_route.route('/health-insurance/id=<int:id>', methods = ['GET'])
def get_health_insurance_by_id(id):
    return get_by_id(id)

@health_insurance_route.route('/health-insurance/add', methods = ['POST'])
def insert_health_insurance():
    return insert()

@health_insurance_route.route('/health-insurance/update/id=<int:id>', methods = ['PUT'])
def update_health_insurance(id):
    return update(id)

@health_insurance_route.route('/health-insurance/delete/id=<int:id>', methods = ['DELETE'])
def delete_health_insurance(id):
    return delete(id)

@health_insurance_route.route('/get-all-patient/account_id=<int:account_id>')
def get_all_patient_by_id(account_id):
    return get_patient_by_id(account_id)