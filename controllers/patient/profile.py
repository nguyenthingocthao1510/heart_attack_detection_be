from dbconfig.app import db
import datetime

class ProfileController:
    @staticmethod
    def calculate_age(year):
        patient_year = int(year.strftime("%Y"))
        current_year = int(datetime.datetime.now().strftime("%Y"))
        age = current_year - patient_year
        return age
    
    @staticmethod
    def get_by_id(account_id):
        cur = db.cursor()
        try:
            cur.execute('SELECT * FROM patient WHERE account_id = %s', (account_id,))
            patient = cur.fetchone()
            if patient:
                dob = patient[4]
                age = ProfileController.calculate_age(dob)

                res = {
                    'id': patient[0],
                    'name': patient[1],
                    'account_id': patient[2],
                    'gender': patient[3],
                    'dob': dob,
                    'age': age
                }
                
                return {'data': res}, 200
            else:
                return {'error':'Patient not found'}, 404
        except Exception as e:
            return (f'Error: {str(e)}')
        finally:
            cur.close()