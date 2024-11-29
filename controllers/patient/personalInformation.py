from dbconfig.app import db

class PersonalInformation:
    @staticmethod
    def get_by_id(account_id):
        cur = db.cursor()
        try:
            cur.execute('SELECT * FROM patient WHERE account_id = %s', (account_id,))
            patient = cur.fetchone()
            if patient:
                res = {
                    'id': patient[0],
                    'name': patient[1],
                    'account_id': patient[2],
                    'gender': patient[3],
                    'dob': patient[4],
                }
                return {'data': res}, 200
            else:
                return {'error':'Patient not found'}, 404
        except Exception as e:
            return (f'Error: {str(e)}')
        finally:
            cur.close()