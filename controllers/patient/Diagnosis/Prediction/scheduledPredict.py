import time, schedule
from config.dbconfig.app import db
from flask import g
from controllers.patient.Diagnosis.Prediction.basePredict import BasePredictor
from controllers.patient.patientRecord.patientRecord import get_latest_record
from middlewares.checkLogin import get_logged_in_user

class ScheduledDiagnosis(BasePredictor):
    def __init__(self):
        super().__init__(
            model_path=r'controllers/patient/Diagnosis/pickle/lr.pkl',
            scaler_path=r'controllers/patient/Diagnosis/pickle/scaler.pkl',
            logger_name="ScheduledDiagnosis"
        )

    def receive_sensor_data(self):
        self.logger.info("Waiting sensor to retrieve data...")
        cur = db.cursor()
        try:
            
            cur.execute('SELECT * FROM sensor_data WHERE account_id = %s ORDER BY id DESC LIMIT 1', )
            sensor_data = cur.fetchone()
            if sensor_data:
                res = {
                    'thalachh': sensor_data[1],
                    'resecg': sensor_data[2]
                }
                self.logger.debug(f"Raw user data received: {res}")
                return {'data': res}, 200
            else:
                return {'error':'Sensor data not found'}, 404
        except Exception as e:
            self.logger.error(f'Error: {str(e)}')
            return
        finally:
            cur.close()

    def receive_user_data(self):
        self.logger.debug(f'Account id: {account_id}')
        if not account_id:
            self.logger.error('User has not logged in')
            return

        user_data = get_latest_record(account_id)
        self.logger.debug(f'User data: {user_data}')
        return user_data

    def predict(self):
        sensor_input = self.receive_sensor_data()
        user_input = self.receive_sensor_data()
        result = self.predict(sensor_input, user_input)
        return result
    
    def run_scheduler(self):
        self.logger.info("Starting scheduler after a brief delay...")
        time.sleep(15)
        self.logger.info("scheduler started...")
        schedule.every(15).seconds.do(self.predict)

        while True:
            try:
                schedule.run_pending()
                time.sleep(1)
            except Exception as e:
                self.logger.error(f"Scheduler encountered an error: {e}")
                self.logger.info("Restarting scheduler...")

