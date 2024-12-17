from controllers.baseRepository import BaseRepository
from flask import request

class DiagnosisHistoryRepo(BaseRepository):
    def __init__(self):
        super().__init__(
            db_table = "diagnosis_history",
            logger = "diagnosisHistory.py"
        )

    def add_by_patient_id(self, patient_id, thalachh, restecg, timestamp):

        try:
            self.cur.execute(f'''
                             INSERT INTO {self.db_table}(patient_id, thalachh, restecg, diagnosis_time) 
                             VALUES (%s, %s, %s, %s)
                             ''', (patient_id, thalachh, restecg, timestamp))
            self.db.commit()
            self.logger.info('"Successfully stored diagnosis history"')
            return {"Successfully stored diagnosis history"}, 200
        except Exception as e:
            self.db.rollback()
            self.logger.error(f'An error occurred: {e}')
            return e
        finally:
            self.cur.close()