from config.dbconfig.app import db
from utils.logger import Logger
import datetime

logger = Logger('profile.py')

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

    @staticmethod
    def check_need_prediction():
        cur = db.cursor()
        try:
            cur.execute('''
                        SELECT id FROM patient WHERE need_prediction = %s
                        ''', 'Yes')
            patients = cur.fetchall()
            if patients:
                result = [p[0] for p in patients]
                logger.debug(f"Patients need prediction: {result}")
                return result
            else:
                logger.error("Patients need prediction not found!")
                return {"Patients need prediction not found!"}, 404
        except Exception as e:
            logger.error(f'Error: {str(e)}')
            return {f'Error: {str(e)}'}, 500
        finally:
            cur.close()