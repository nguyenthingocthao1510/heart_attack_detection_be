from controllers.baseRepository import BaseRepository
from flask import request, jsonify

class DiagnosisHistoryRepo(BaseRepository):
    def __init__(self):
        super().__init__(
            db_table = "diagnosis_history",
        )

    def add_by_patient_id(self, patient_id, result, thalachh, restecg, diagnosis_time):
        cur = self._get_cursor()
        try:
            cur.execute(f'''
                            INSERT INTO {self.db_table}(patient_id, result, thalachh, restecg, diagnosis_time) 
                            VALUES (%s, %s, %s, %s)
                        ''', (patient_id, result, thalachh, restecg, diagnosis_time))
            self.db.commit()
            self.logger.info('"Successfully stored diagnosis history"')
            return {"Successfully stored diagnosis history"}, 200
        except Exception as e:
            self.db.rollback()
            self.logger.error(f'An error occurred: {e}')
            return e
        finally:
            cur.close()

    def save_diagnosis_history(self):
        if request.method == 'POST':
            data = request.get_json()
            cur = self._get_cursor()
            try:
                cur.execute(f'''
                                INSERT INTO {self.db_table}(patient_id, result, thalachh, restecg, diagnosis_time) 
                                VALUES (%s, %s, %s, %s, %s)
                            ''', (data['patient_id'], data['prediction'], data['thalachh'], data['restecg'], data['timestamp']))
                self.db.commit()
                self.logger.info('"Successfully stored diagnosis history"')
                return data, 200
            except Exception as e:
                self.db.rollback()
                self.logger.error(f'An error occurred: {e}')
                return e
            finally:
                cur.close()
