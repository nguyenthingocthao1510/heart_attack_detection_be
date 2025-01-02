from controllers.baseRepository import BaseRepository
from controllers.patient.profile.profile import ProfileRepo

class SensorRepo(BaseRepository):
    def __init__(self):
        super().__init__(
            db_table = 'sensor_data',
        )

        self.profile_repo = ProfileRepo()

    def receive_sensor_data(self):
        patient_id = self.profile_repo.check_need_prediction()
        cur = self._get_cursor()
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
                    f"No sensor data found for patient_id: {id}"

            if result:
                return result
            else:
                return {"error": "No sensor data found for any patients"}, 404
        except Exception as e:
            return {"error": str(e)}, 500
        finally:
            cur.close()