from controllers.baseRepository import BaseRepository

class DiagnosisHistoryRepo(BaseRepository):
    def __init__(self):
        super().__init__(db_table = "diagnosis_history")

    def add_by_patient_id(self, tb_id, patient_id, thalachh, restecg, timestamp):
        try:
            self.cur.execute(f'''
                             INSERT INTO {self.db_table}(id, thalachh, restecg, timestamp) 
                             VALUES ({tb_id}, {thalachh}, {restecg}, {timestamp})
                             WHERE patient_id = {patient_id}
                             ''')
            return
        except Exception as e:
            return e
        finally:
            self.cur.close()