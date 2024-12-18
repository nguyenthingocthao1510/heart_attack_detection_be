from flask import request
from config.dbconfig.app import db
from utils.logger import Logger
from controllers.baseRepository import BaseRepository
import datetime

logger = Logger()

class ProfileRepo(BaseRepository):
    def __init__(self):
        super().__init__(
            db_table = 'patient',
        )
        
    def calculate_age(self, year):
        patient_year = int(year.strftime("%Y"))
        current_year = int(datetime.datetime.now().strftime("%Y"))
        age = current_year - patient_year
        return age
    
    def get_by_id(self, account_id):
        cur = self._get_cursor()
        try:
            cur.execute('SELECT * FROM patient WHERE account_id = %s', (account_id,))
            patient = cur.fetchone()
            if patient:
                dob = patient[4]
                age = self.calculate_age(dob)

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

    def check_need_prediction(self):
        cur = self._get_cursor()
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

    def update_need_prediction(self):
        data = request.get_json()
        cur = self._get_cursor()
        try:
            super().update('need_prediction = %s', 
                           'id = %s', 
                           (data['need_prediction'], data['id']))

            self.logger.debug(f'Update need_prediction to {data['need_prediction']} successfully!')
            return f'Update need_prediction to {data['need_prediction']} successfully!', 200
        except Exception as e:
            self.logger.error(f'An error occurred: {e}')
            return f'An error occurred: {e}', 500
        finally:
            cur.close()