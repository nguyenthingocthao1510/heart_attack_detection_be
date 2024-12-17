import time, schedule
from config.dbconfig.app import db
from controllers.patient.diagnosis.prediction.basePredict import BasePredictor
from controllers.patient.patientRecord.patientRecord import get_record_by_patient_id

class ScheduledDiagnosis(BasePredictor):
    def __init__(self):
        super().__init__(
            model_path=r'controllers/patient/Diagnosis/Prediction/pickle/lr.pkl',
            scaler_path=r'controllers/patient/Diagnosis/Prediction/pickle/scaler.pkl',
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
                    self.logger.debug(f"No sensor data found for patient_id: {id}")

            if result:
                self.logger.debug(f"Sensor data received: {result}")
                return result
            else:
                return {"error": "No sensor data found for any patients"}, 404
        except Exception as e:
            self.logger.error(f'Error: {str(e)}')
            return {"error": str(e)}, 500
        finally:
            cur.close()

    def receive_user_data(self):
        patient_id = self.check_need_prediction()
        cur = db.cursor()
        result = []
        try:
            for id in patient_id:
                record = get_record_by_patient_id(id)
                if record:
                    result.append({
                        'patient_id':id,
                        'age': record[0],
                        'trtbps': record[1],
                        'chol': record[2],
                        'oldpeak': record[3],
                        'sex': record[4],
                        'exng': record[5],
                        'caa': record[6],
                        'cp': record[7],
                        'fbs': record[8],
                        'slp': record[9],
                        'thall': record[10]
                    })
                else:
                    self.logger.debug(f"No record found for patient_id: {patient_id}")

            if result:
                self.logger.debug(f"Patient record data received: {result}")
                return result
            else:
                return {"error": "No record data found for any patients"}, 404
        except Exception as e:
            self.logger.error(f'Error: {str(e)}')
            return {"error": str(e)}, 500
        finally:
            cur.close()
    
    def combine_data(self, sensor_input, user_input):
        lookup = {id['patient_id']: id for id in user_input}

        combined_data = []
        for id in sensor_input:
            pid = id['patient_id']
            if pid in lookup:
                merged = {**id, **lookup[pid]}
                combined_data.append(merged)

        self.logger.debug(f'Combined data: {combined_data}')
        return combined_data

    def predict(self):
        sensor_input = self.receive_sensor_data()
        user_input = self.receive_user_data()
        combined_data = self.combine_data(sensor_input, user_input)

        result_list = []
        for cd in combined_data:
            result = super().predict(cd)
            result_list.append(result)
        self.logger.debug(f'Result list: {result_list}')
        return result_list
    
    def run_scheduler(self):
        self.logger.info("Starting scheduler after a brief delay...")
        time.sleep(5)
        self.logger.info("scheduler started...")
        schedule.every(45).seconds.do(self.predict)

        while True:
            try:
                schedule.run_pending()
                time.sleep(1)
            except Exception as e:
                self.logger.error(f"Scheduler encountered an error: {e}")
                self.logger.info("Restarting scheduler...")

