from flask import jsonify, request
from dbconfig.app import db

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
                'account_id': d[2]
            })
        return jsonify({'data': result}), 200
    except Exception as e:
        return jsonify({'Error': str(e)}), 500
    finally:
        cur.close()