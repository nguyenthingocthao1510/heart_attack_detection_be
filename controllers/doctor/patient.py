from dbconfig.app import db
from flask import request

#GET ALL
def get_all():
    cur = db.cursor()
    try:
            cur.execute('SELECT * FROM patient')
            patients = cur.fetchall()
            result = []
            for patient in patients:
                result.append({
                    'id': patient[0],
                    'name': patient[1]
                })
            return {'data': result}, 200
    except Exception as e:
            return (f'Error: {str(e)}')
    finally:
            cur.close()

#GET BY ID
def get_by_id(id):
    if request.method == 'GET':
        cur = db.cursor()
        try:
            cur.execute('SELECT * FROM patient WHERE id = %s', (id,))
            patient = cur.fetchone()

            if patient:
                res = {
                'id' : patient[0],
                'name': patient[1]
                }
                return {'data': res}, 200
            else:
                return {'error':'Patient not found'}, 404
        except Exception as e:
            return (f'Error: {str(e)}')
        finally:
            cur.close()

#INSERT
def add():
    if request.method == 'POST':
        data = request.get_json()
        name = data['name']

        cur = db.cursor()
        try:
            cur.execute('INSERT INTO patient(name) VALUES (%s)', (name))
            db.commit()
            return {'data': data}, 200
        except Exception as e:
            db.rollback()
            return (f'Error: {str(e)}')
        finally:
            cur.close()

#UPDATE
def update(id):
    if request.method == 'PUT':
        data = request.get_json()
        name = data['name']

        cur = db.cursor()
        try:
            cur.execute('UPDATE patient SET name = %s WHERE id = %s', (name, id))
            db.commit()
            
            if cur.rowcount > 0:  
                return {'data': data}, 200
            else:
                return ('ID not found', 404) 
        except Exception as e:
            db.rollback()
            return (f'Error: {str(e)}', 500) 
        finally:
            cur.close()

#DELETE
def delete(id):
    if request.method == 'DELETE':
        cur = db.cursor()
        try:
            cur.execute('DELETE FROM patient WHERE id = %s', (id,))
            db.commit()
            if cur.rowcount > 0:
                return {'message': 'Delete successfully'}, 200
            else:
                return {'error' : 'Patient ID not found'}, 404
        except Exception as e:
            db.rollback()
            return {'error' : str(e)}, 500
        finally:
            cur.close()
