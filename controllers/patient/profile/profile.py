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
                    'age': age,
                    'need_prediction': patient[5],
                    'phone_number': patient[6],
                    'email': patient[7],
                    'address': patient[8]
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
                return result
            else:
                return {"Patients need prediction not found!"}, 404
        except Exception as e:
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

            return {f"Update need_prediction to {data['need_prediction']} successfully!"}, 200
        except Exception as e:
            self.db.rollback()
            return {f"An error occurred: {e}"}, 500
        finally:
            cur.close()