from flask import request, jsonify
import pymysql
import time

hostname = 'byidr5v6nlhpekvrv8og-mysql.services.clever-cloud.com'
user = 'ubidznrunxwyuqke'
password = 'SMC7p0rv3J09jZ4ThuU1'
database = 'byidr5v6nlhpekvrv8og'


def get_heartbeat():
    cursor = None
    connection = None
    try:
        # Mở kết nối mới mỗi lần request
        connection = pymysql.connect(host=hostname, user=user, password=password, db=database)
        cursor = connection.cursor()

        cursor.execute('''
            SELECT SQL_NO_CACHE id, device_id, thalachh, restecg, avg_bpm, timestamp
            FROM sensor_data
            ORDER BY timestamp DESC
            LIMIT 5;
        ''')
        heartbeat = cursor.fetchall()

        result = [
            {'id': h[0], 'device_id': h[1], 'thalachh': h[2], 'restecg': h[3], 'avg_bpm': h[4], 'timestamp': h[5]}
            for h in heartbeat
        ]
        return jsonify({'data': result, 'timestamp': time.time()}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def get_avg_BPM():
    cursor = None
    connection = None
    try:
        connection = pymysql.connect(host=hostname, user=user, password=password, db=database)
        cursor = connection.cursor()

        cursor.execute('''
            SELECT id, device_id, avg_bpm, timestamp
            FROM sensor_data
            ORDER BY timestamp DESC
            LIMIT 5;
        ''')
        data = cursor.fetchall()

        result = [
            {'id': d[0], 'device_id': d[1], 'avg_bpm': d[2], 'timestamp': d[3]}
            for d in data
        ]

        return jsonify({'data': result, 'timestamp': time.time()}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
