from flask import jsonify, request
from config.dbconfig.app import db

def get_all():
    cur = db.cursor()
    try:
        cur.execute('SELECT * FROM medicine')
        medicines = cur.fetchall()
        result = []
        for m in medicines:
            result.append({
                'id': m[0],
                'name': m[1],
                'uses': m[2],
                'description': m[3],
            })
        return jsonify({'data': result}),200
    except Exception as e:
        print(f'Error: {str(e)}')
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()

def get_by_id(id):
    cur = db.cursor()
    try:
        cur.execute('SELECT * FROM medicine WHERE id = %s', (id))
        medicine = cur.fetchone()

        if medicine:
            res = {
                'id': medicine[0],
                'name': medicine[1],
                'uses': medicine[2],
                'description': medicine[3],
            }
            return jsonify({'data': res}),200
        else:
            return jsonify({'error': 'Medicine not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()

def add():
    if request.method == 'POST':
        cur = db.cursor()
        data = request.get_json()
        name = data['name']
        uses  = data['uses']
        description = data['description']

        try:
            cur.execute('INSERT INTO medicine (name, uses, description) VALUES (%s,%s,%s)',(name, uses, description))
            db.commit()
            return jsonify({'data': data}), 200
        except Exception as e:
            db.rollback()
            return jsonify({'error': str(e)}),500
        finally:
            cur.close()


def update(id):
    if request.method == 'PUT':
        cur = db.cursor()
        data = request.get_json()
        name = data['name']
        uses  = data['uses']
        description = data['description']

        try:
            cur.execute('UPDATE medicine SET name = %s, uses = %s, description = %s WHERE id = %s',(name, uses, description,id))
            db.commit()
            return jsonify({'data': data}), 200
        except Exception as e:
            db.rollback()
            return jsonify({'error': str(e)}),500
        finally:
            cur.close()

def delete(id):
    if request.method == 'DELETE':
        cur = db.cursor()
        try:
            cur.execute('DELETE FROM medicine WHERE id = %s', (id))
            db.commit()
            return {'message': 'Delete successfully'}, 200
        except Exception as e:
            db.rollback()
            return jsonify({'Error': str(e)}), 500
        finally:
            cur.close()





