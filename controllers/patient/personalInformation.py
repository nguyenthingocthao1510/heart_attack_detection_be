from dbconfig.app import db
from flask import request

class PatientPersonalInformationController:
    @staticmethod
    def get_by_id(patient_id):
        if request.method == 'GET':
            cur = db.cursor()
            try:
                cur.execute('SELECT * FROM patient WHERE patient_id = %s', (id,))
                patient = cur.fetchone()

                if patient:
                    res = {
                    'patient_id' : patient[0],
                    'patient_name': patient[1],
                    'patient_gender': patient[2],
                    'patient_dob': patient[3],
                    }
                    return {'data': res}, 200
                else:
                    return {'error':'Patient not found'}, 404
            except Exception as e:
                return (f'Error: {str(e)}')
            finally:
                cur.close()