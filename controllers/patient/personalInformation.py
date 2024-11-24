from dbconfig.app import db

class PersonalInformation:
    @staticmethod
    def get_by_id(patient_id):
        cur = db.cursor()
        try:
            cur.execute('SELECT * FROM patient WHERE id = %s', (patient_id,))
            patient = cur.fetchone()
            if patient:
                res = {
                    'patient_id': patient[0],
                    'name': patient[1],
                    'gender': patient[2],
                    'dob': patient[3],
                }
                return {'data': res}, 200
            else:
                return {'error':'Patient not found'}, 404
        except Exception as e:
            return (f'Error: {str(e)}')
        finally:
            cur.close()