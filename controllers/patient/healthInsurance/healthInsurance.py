from flask import request, jsonify
from config.dbconfig.app import db

def get_all(account_id):
    cursor = db.cursor()
    try:
        cursor.execute('SELECT hi.id, hi.health_insurance_id,  p.name FROM health_insurance hi JOIN patient p ON p.id = hi.patient_id WHERE hi.account_id = %s',(account_id))
        data = cursor.fetchall()
        result = []

        for d in data:
            result.append({
                'id': d[0],
                'health_insurance_id': d[1],
                'name': d[2]
            })
            return {'data' : result}, 200
    except Exception as e:
        return (f'error: {str(e)}')
    finally:
        cursor.close()
    
def get_by_id(id):
    cursor = db.cursor()
    try:
        cursor.execute('SELECT * FROM health_insurance WHERE id = %s',(id))
        data = cursor.fetchone()
        if data:
            res = {
                'id': data[0],
                'patient_id': data[1],
                'account_id': data[2],
                'registration_place': data[3],
                'shelf_life': data[4],
                'five_years_insurance': data[5],
                'place_provide': data[6],
                'create_date': data[7],
                'modified_by': data[8],
                'health_insurance_id': data[9]
            }
            return jsonify({'data': res}), 200
        else:
            return jsonify({'error': 'not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()

def insert():
    if request.method == 'POST':
        cursor = db.cursor()
        data = request.get_json()
        patient_id = data['patient_id']
        account_id = data['account_id']
        registration_place = data['registration_place']
        shelf_life = data['shelf_life']
        five_years_insurance = data['five_years_insurance']
        place_provide = data['place_provide']
        create_date = data['create_date']
        modified_by = data['modified_by']
        health_insurance_id = data['health_insurance_id']

        try:
            cursor.execute('INSERT INTO health_insurance (patient_id, account_id, registration_place, shelf_life, five_years_insurance, place_provide, create_date, modified_by, health_insurance_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)', (patient_id, account_id, registration_place, shelf_life, five_years_insurance, place_provide, create_date, modified_by, health_insurance_id))
            db.commit()
            return jsonify({'data': data}), 200
        except Exception as e:
            db.rollback()
            return jsonify({'error': str(e)}), 500
        finally:
            cursor.close()

def update(id):
    if request.method == 'PUT':
        cur = db.cursor()
        data = request.get_json()
        registration_place = data['registration_place']
        shelf_life = data['shelf_life'] 
        five_years_insurance = data['five_years_insurance']
        place_provide = data['place_provide']
        create_date = data['create_date']
        modified_by = data['modified_by']
        health_insurance_id = data['health_insurance_id']

        try:
            cur.execute('UPDATE health_insurance SET registration_place = %s, shelf_life = %s, five_years_insurance = %s, place_provide = %s, create_date = %s, modified_by = %s, health_insurance_id = %s WHERE id = %s ',(registration_place, shelf_life, five_years_insurance, place_provide, create_date, modified_by, health_insurance_id, id))
            db.commit()
            return jsonify({'data': data}), 200
        except Exception as e:
            db.rollback()
            return jsonify({'error': str(e)}), 500
        finally:
            cur.close()

#DELETE
def delete(id):
      if request.method == 'DELETE':
            cur = db.cursor()        
            try:
                  cur.execute('DELETE FROM health_insurance WHERE id = %s', (id))
                  if cur.rowcount > 0:
                    return {'message': 'Delete successfully'}, 200
                  else:
                       return {'error' : 'Health insurance ID not found'}, 404
            except Exception as e:
                 db.rollback()
                 return {'error' : str(e)}, 500
            finally:
                cur.close()
                   

def get_patient_by_id(account_id):
    cursor = db.cursor()
    try:
        cursor.execute('SELECT id FROM patient WHERE account_id = %s',(account_id))
        data = cursor.fetchone()
        if data:
            res = {
                'id': data[0],
            }
            return jsonify({'data': res}), 200
        else:
            return jsonify({'error': 'not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()


