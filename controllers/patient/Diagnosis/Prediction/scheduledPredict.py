import time, schedule
from config.dbconfig.app import db
from controllers.patient.Diagnosis.Prediction.basePredict import BasePredictor
from controllers.patient.patientRecord.patientRecord import get_latest_record

class ScheduledDiagnosis(BasePredictor):
    def __init__(self):
        super().__init__(
            model_path=r'controllers/patient/Diagnosis/pickle/lr.pkl',
            scaler_path=r'controllers/patient/Diagnosis/pickle/scaler.pkl',
            logger_name="ScheduledDiagnosis"
        )

    def check_need_prediction(self):
        cur = db.cursor()
        try:
            cur.execute('''
                        SELECT id FROM patient WHERE need_prediction = %s
                        ''', 'Yes')
            patients = cur.fetchall()
            if patients:
                result = [p[0] for p in patients]
                self.logger.debug(f"Patients need prediction: {result}")
                return result
            else:
                self.logger.error("Patients need prediction not found!")
                return {"Patients need prediction not found!"}, 404
        except Exception as e:
            self.logger.error(f'Error: {str(e)}')
            return {f'Error: {str(e)}'}, 500
        finally:
            cur.close()

    def receive_sensor_data(self):
        patient_id = self.check_need_prediction()
        self.logger.debug(f'patient id: {patient_id}')
        cur = db.cursor()
        result = []
        try:
            for id in patient_id:
                cur.execute('''
                            SELECT sd.thalachh, sd.restecg
                            FROM sensor_data sd 
                            JOIN device d ON sd.device_id = d.id
                            WHERE patient_id = %s 
                            ORDER BY sd.id DESC 
                            LIMIT 1
                            ''', (id,))
                sensor = cur.fetchone() 
                if sensor:
                    result.append({
                        'patient_id': id,
                        'thalachh': sensor[0],
                        'restecg': sensor[1],
                    })
                else:
                    self.logger.debug(f"No sensor data found for patient_id: {patient_id}")

            if result:
                self.logger.debug(f"Sensor data received: {result}")
                return result, 200
            else:
                return {"error": "No sensor data found for any patients"}, 404
        except Exception as e:
            self.logger.error(f'Error: {str(e)}')
            return {"error": str(e)}, 500
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

