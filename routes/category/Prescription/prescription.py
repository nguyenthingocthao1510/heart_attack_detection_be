from flask import Blueprint
from controllers.category.Prescription.prescription import get_all, get_by_id, create_prescription, update_prescription_detail, delete
prescription_route = Blueprint('prescription_route', __name__)

@prescription_route.route('/prescriptions/accountId=<int:account_id>' , methods = ['GET'])
def get_all_prescription(account_id):
    return get_all(account_id)

@prescription_route.route('/prescription/accountId=<int:account_id>/prescriptionId=<int:prescription_id>' , methods = ['GET'])
def get_prescription_by_id(account_id, prescription_id):
    return get_by_id(account_id, prescription_id)

@prescription_route.route('/prescription/create-prescription' , methods = ['POST'])
def create_new_prescription():
    return create_prescription()

@prescription_route.route('/prescription/update-prescription/<int:prescription_id>', methods=['PUT'])
def update_prescription(prescription_id):
    return update_prescription_detail(prescription_id)

@prescription_route.route('/prescription/delete-prescription/prescriptionId=<int:id>' , methods = ['DELETE'])
def delete_prescription_detail(id):
    return delete(id)

