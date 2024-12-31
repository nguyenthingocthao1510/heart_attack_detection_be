from controllers.baseRepository import BaseRepository
from collections import defaultdict
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
            return {"Successfully stored diagnosis history"}, 200
        except Exception as e:
            self.db.rollback()
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
                return data, 200
            except Exception as e:
                self.db.rollback()
                return e
            finally:
                cur.close()
    
    def get_history(self, patient_id: int):
        cur = self._get_cursor()
        try:
            cur.execute(
                """
                    SELECT 
                        DATE(diagnosis_time) AS diagnosis_date,
                        diagnosis_time,
                        restecg,
                        result,
                        thalachh
                    FROM 
                        diagnosis_history
                    WHERE 
                        patient_id = %s
                    ORDER BY 
                        diagnosis_date DESC, 
                        diagnosis_time DESC
                """,
                (patient_id,)
            )        
            
            raw_data = cur.fetchall()
            history_dict = defaultdict(list)
            for record in raw_data:
                diagnosis_date = record[0]
                entry = {
                    'diagnosis_time': record[1],
                    'restecg': record[2],
                    'result': record[3],
                    'thalachh': record[4]
                }
                history_dict[diagnosis_date].append(entry)
            
            history = [
                {'date': date, 'entries': entries}
                for date, entries in history_dict.items()
            ]

            return jsonify({"history": history}), 200
        except Exception as e:
            return f"An error occurred: {e}", 500
        finally:
            cur.close()