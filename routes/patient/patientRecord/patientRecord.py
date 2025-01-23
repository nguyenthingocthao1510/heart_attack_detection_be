from flask import Blueprint
from controllers.patient.patientRecord.patientRecord import get_records_history, get_all_patient_form, get_history_patient_record, get_latest_record, insert, update, get_patient_record, get_for_list

patient_record_route = Blueprint('patient_record_route', __name__)

# DOCTOR
@patient_record_route.route('/patient-records/accountId=<int:account_id>', methods=['GET'])
def get_all_patient_record_form(account_id):
    return get_all_patient_form(account_id)

@patient_record_route.route('/patient-history-records/accountId=<int:account_id>/patientId=<int:patient_id>', methods=['GET'])
def get_history_patient_record_form(account_id,patient_id):
    return get_history_patient_record(account_id,patient_id)

@patient_record_route.route('/patient-record/id=<int:id>', methods=['GET'])
def get_doctor_patient_record(id):
    return get_patient_record(id)

@patient_record_route.route('/patient-record/list-patient-records', methods=['POST'])
def filter_patient_record():
    return get_for_list()

@patient_record_route.route('/patient-records/add', methods=['POST'])
def create_new_patient_record():
    return insert()

@patient_record_route.route('/patient-record/update/id=<int:id>', methods=['PUT'])
def update_patient_record(id):
    return update(id)

# PATIENT
@patient_record_route.route('/latest-patient-record/accountId=<int:account_id>', methods=['GET'])
def get_latest_patient_record(account_id):
    return get_latest_record(account_id, 'd')

@patient_record_route.route('/latest-patient-record2/accountId=<int:account_id>', methods=['GET'])
def get_latest_patient_record2(account_id):
    return get_latest_record(account_id, 'pr')

@patient_record_route.route('/records/accountId=<int:account_id>', methods=['GET'])
def get_all_patient_record_history(account_id):
    return get_records_history(account_id)


