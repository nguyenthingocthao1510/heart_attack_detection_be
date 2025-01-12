from flask import jsonify, request
from config.dbconfig.app import db

def get_all():
    cur = db.cursor()
    try:
        cur.execute('SELECT * FROM doctor')
        doctors = cur.fetchall()
        result = []
        for d in doctors:
            result.append({
                'id': d[0],
                'name': d[1],
                'account_id': d[2],
                'dob': d[3],
                'gender': d[4],
                'specialization': d[5],
                'email': d[6],
                'address': d[7],
                'age': d[8]
            })
        return jsonify({'data': result}), 200
    except Exception as e:
        return jsonify({'Error': str(e)}), 500
    finally:
        cur.close()

def get_for_list():
    if request.method == 'POST':
        cursor = db.cursor()
        data = request.json
        name = data.get('name')

        try:
            cursor.execute("SELECT * FROM doctor WHERE name LIKE %s", (f"%{name}%",))
            doctors = cursor.fetchall()

            result = []
            for d in doctors:
                result.append({
                    'id': d[0],
                    'name': d[1],
                    'account_id': d[2],
                    'dob': d[3],
                    'gender': d[4],
                    'specialization': d[5],
                    'email': d[6],
                    'address': d[7],
                    'age': d[8]
                })

            return jsonify({'data': result})

        except Exception as e:
            print(f"Error occurred: {str(e)}")
            return jsonify({'error': str(e)}), 500

        finally:
            cursor.close()

def get_by_id(account_id):
    cur = db.cursor()
    try:
        cur.execute('SELECT * FROM doctor WHERE account_id = %s',(account_id))
        doctor = cur.fetchone()
        
        if doctor:
            res = {
                'id': doctor[0],
                'name': doctor[1],
                'account_id': doctor[2],
                'dob': doctor[3],
                'gender': doctor[4],
                'specialization': doctor[5],
                'email': doctor[6],
                'address': doctor[7],
                'age': doctor[8]
            }
            return jsonify({'data': res}), 200
        else:
            return jsonify({'Error': 'Doctor not found'}), 404
    except Exception as e:
        return jsonify({'Error': str(e)}), 500
    finally:
        cur.close()
    
def create():
    if request.method == 'POST':
        cur = db.cursor()
        data = request.get_json()
        name =  data['name']
        account_id =  data['account_id']
        dob =  data['dob']
        gender =  data['gender']
        specialization =  data['specialization']
        email =  data['email']
        address =  data['address']
        age =  data['age']

        try:
            cur.execute('INSERT INTO doctor (name, account_id, dob, gender, specialization, email, address, age) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)', (name, account_id, dob, gender, specialization, email, address, age))
            db.commit()
            return jsonify({'data': data}), 200
        except Exception as e:
            db.rollback()
            return jsonify({'Error': str(e)}), 500
        finally:
            cur.close()

def update(id):
    if request.method == 'PUT':
        cur = db.cursor()
        data = request.get_json()
        name =  data['name']
        dob =  data['dob']
        gender =  data['gender']
        specialization =  data['specialization']
        email =  data['email']
        address =  data['address']
        age =  data['age']

        try:
            cur.execute('UPDATE doctor SET name = %s, dob = %s, gender = %s, specialization = %s, email = %s, address = %s, age = %s WHERE id = %s',(name, dob, gender, specialization, email, address, age, id))
            db.commit()
            return jsonify({'data': data}), 200
        except Exception as e:
            db.rollback()
            return jsonify({'error': str(e)}), 500
        finally:
            cur.close()

def delete():
    return 0




