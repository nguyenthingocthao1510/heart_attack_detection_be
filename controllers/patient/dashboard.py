from flask import request, jsonify
from config.dbconfig.app import db


def get_heartbeat():
    cursor = db.cursor()
    try:
        cursor.execute('''
            SELECT * 
            FROM sensor_data
            ORDER BY timestamp DESC 
            LIMIT 5;
        ''')
        heartbeat = cursor.fetchall()
        result = []
        for h in heartbeat:
            result.append({
                'id': h[0],
                'device_id': h[1],
                'thalachh': h[2],
                'restecg': h[3],
                'avg_bpm': h[4],
                'timestamp': h[5],
            })
        return jsonify({'data': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()

def get_avg_BPM():
    cursor = db.cursor()
    try:
        cursor.execute('''
            SELECT id, device_id, avg_bpm, timestamp
            FROM sensor_data
            ORDER BY timestamp DESC 
            LIMIT 5;
        ''')
        data = cursor.fetchall()
        result = []
        for d in data:
            result.append({
                'id': d[0],
                'device_id': d[1],
                'avg_bpm': d[2],
                'timestamp': d[3],
            })
        return jsonify({'data': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()