from flask import jsonify, request
from dbconfig.app import db

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
