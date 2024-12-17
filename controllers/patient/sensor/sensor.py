from controllers.baseRepository import BaseRepository
from controllers.patient.profile import ProfileController

class SensorRepo(BaseRepository):
    def __init__(self):
        super().__init__(
            db_table = 'sensor_data',
            logger = 'sensor.py'
        )

        self.profile_controller = ProfileController()

    def receive_sensor_data(self):
        patient_id = self.profile_controller.check_need_prediction()
        result = []
        try:
            for id in patient_id:
                self.cur.execute('''
                                SELECT sd.thalachh, sd.restecg
                                FROM sensor_data sd 
                                JOIN device d ON sd.device_id = d.id
                                WHERE patient_id = %s 
                                ORDER BY sd.id DESC 
                                LIMIT 1
                                ''', (id,))
                sensor = self.cur.fetchone() 
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
            self.cur.close()