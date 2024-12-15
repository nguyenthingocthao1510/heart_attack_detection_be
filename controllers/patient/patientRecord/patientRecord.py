from flask import request, jsonify, Blueprint
from config.dbconfig.app import db
from pymysql.cursors import DictCursor

## DOCTOR
# GET ALL PATIENT FORM - DOCTOR
def get_all_patient_form(account_id):
    cursor = db.cursor(DictCursor)

    try:
        # Xác định vai trò user
        cursor.execute(
            '''
            SELECT 
                COALESCE(d.id, p.id) AS user_id,
                CASE 
                    WHEN d.id IS NOT NULL THEN 'doctor'
                    WHEN p.id IS NOT NULL THEN 'patient'
                END AS role
            FROM account a
            LEFT JOIN doctor d ON d.account_id = a.id
            LEFT JOIN patient p ON p.account_id = a.id
            WHERE a.id = %s
        ''', (account_id,))
        print(f'account_id: {account_id}')

        result = cursor.fetchone()

        print(f'result: {result}')

        if not result:
            return jsonify({'error': 'Account not found'}), 400
        
        user_id, role = result['user_id'], result['role']

        if role == 'doctor':
            # Truy vấn danh sách hồ sơ bệnh án mới nhất
            cursor.execute(
                '''
                SELECT p.*, pr.doctor_id AS doctor_id, pr.id as patient_record_id
                FROM patient_record pr
                JOIN (
                    SELECT patient_id, MAX(id) AS last_id
                    FROM patient_record
                    WHERE doctor_id = %s
                    GROUP BY patient_id
                ) latest_records ON pr.id = latest_records.last_id JOIN patient p on p.id = pr.patient_id
                ORDER BY pr.id DESC
                ''',
                (user_id,)
            )

            patient_record = cursor.fetchall()

            return jsonify({
                'data': patient_record
            }), 200

        else:
            return jsonify({'error': 'Invalid role'}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        cursor.close()

# GET HISTORY OF ONE PATIENT FORM - DOCTOR
def get_history_patient_record(account_id, patient_id):
    cursor = db.cursor(DictCursor)
    try:
        cursor.execute("""
            SELECT 
                COALESCE(d.id, p.id) AS user_id,
                CASE 
                    WHEN d.id IS NOT NULL THEN 'doctor'
                    WHEN p.id IS NOT NULL THEN 'patient'
                END AS role
            FROM account a
            LEFT JOIN doctor d ON d.account_id = a.id
            LEFT JOIN patient p ON p.account_id = a.id
            WHERE a.id = %s
        """, (account_id,))
        result = cursor.fetchone()
        print(f'account_id: {account_id}')
        print(f'result: {result}')

        if not result:
            return jsonify({"error": "Account not found"}), 404

        user_id, role = result['user_id'], result['role']

        if role == 'doctor':
            cursor.execute("""
                SELECT * 
                FROM patient_record 
                WHERE doctor_id = %s AND patient_id = %s
            """, (user_id, patient_id))
            history = cursor.fetchall()
        else:
            return jsonify({"error": "Invalid role"}), 400

        return jsonify({
            "history": history
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()

def get_patient_record(id):
    cursor = db.cursor()
    try:
        cursor.execute('SELECT * FROM patient_record WHERE id = %s', (id))
        patientRecord = cursor.fetchone()

        if patientRecord:
            res = {
                'id': patientRecord[0],
                'doctor_id': patientRecord[1],
                'patient_id': patientRecord[2],
                'account_id': patientRecord[3],
                'age': patientRecord[4],
                'trtbps': patientRecord[5],
                'chol': patientRecord[6],
                'thalachh': patientRecord[7],
                'oldpeak': patientRecord[8],
                'sex': patientRecord[9],
                'exng': patientRecord[10],
                'caa': patientRecord[11],
                'cp': patientRecord[12],
                'fbs': patientRecord[13],
                'restecg': patientRecord[14],
                'slp': patientRecord[15],
                'thall': patientRecord[16],
                'create_date': patientRecord[17],
            }
            return jsonify({'data': res}), 200
        else:
            return jsonify({'error': 'Patient record not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()

# INSERT A NEW PATIENT RECORD
def insert():
    if request.method == 'POST':
        cursor = db.cursor()
        data = request.get_json()
        doctor_id = data['doctor_id']
        patient_id = data['patient_id']
        account_id = data['account_id']
        age = data['age']
        trtbps = data['trtbps']
        chol = data['chol']
        thalachh = data['thalachh']
        oldpeak = data['oldpeak']
        sex = data['sex']
        exng = data['exng']
        caa = data['caa']
        cp = data['cp']
        fbs = data['fbs']
        restecg = data['restecg']
        slp = data['slp']
        thall = data['thall']
        create_date = data['create_date']

        try:
            cursor.execute(
                '''
                   INSERT INTO patient_record
                    (doctor_id, patient_id, account_id, age, trtbps, chol, thalachh, oldpeak, sex, exng, caa, cp, fbs, restecg, slp, thall, create_date)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ''',
                (doctor_id, patient_id, account_id, age, trtbps, chol, thalachh, oldpeak, sex, exng, caa, cp, fbs, restecg, slp, thall, create_date)
            )
            db.commit()
            return jsonify({'data': data}), 200
        except Exception as e:
            db.rollback()
            return jsonify({'error': str(e)})
        finally:
            cursor.close()
        
# UPDATE A PATIENT RECORD
def update(id):
    if request.method == 'PUT':
        cursor = db.cursor()
        data = request.get_json()

        age = data['age']
        trtbps = data['trtbps']
        chol = data['chol']
        thalachh = data['thalachh']
        oldpeak = data['oldpeak']
        sex = data['sex']
        exng = data['exng']
        caa = data['caa']
        cp = data['cp']
        fbs = data['fbs']
        restecg = data['restecg']
        slp = data['slp']
        thall = data['thall']

        try:
            cursor.execute(
                '''
                UPDATE patient_record SET 
                    age = %s, 
                    trtbps = %s, 
                    chol = %s, 
                    thalachh = %s, 
                    oldpeak = %s, 
                    sex = %s, 
                    exng = %s, 
                    caa = %s, 
                    cp = %s, 
                    fbs = %s, 
                    restecg = %s, 
                    slp = %s, 
                    thall = %s 
                WHERE id = %s
                ''',
                (
                    age, 
                    trtbps, 
                    chol, 
                    thalachh, 
                    oldpeak, 
                    sex, 
                    exng, 
                    caa, 
                    cp, 
                    fbs, 
                    restecg, 
                    slp, 
                    thall, 
                    id
                )
            )
            db.commit()
            return jsonify({'data': data}), 200
        except Exception as e:
            db.rollback()
            return jsonify({'error': str(e)}), 500
        finally:
            cursor.close()

## PATIENT
# GET LATEST RECORD - PATIENT
def get_latest_record(account_id):
    cursor = db.cursor(DictCursor)
    
    try:
        cursor.execute(
            '''
            SELECT 
                COALESCE(d.id, p.id) AS user_id,
                CASE
                    WHEN d.id IS NOT NULL THEN 'doctor'
                    WHEN p.id IS NOT NULL THEN 'patient'
                END AS role
            FROM account a
            LEFT JOIN doctor d ON d.account_id = a.id
            LEFT JOIN patient p ON p.account_id = a.id
            WHERE a.id = %s
            ''', (account_id)
        )
        result = cursor.fetchone()

        if not result:
            return jsonify({'error': 'Account not found'}), 404
        
        user_id, role = result['user_id'], result['role']

        if role == 'patient':
            cursor.execute(
                '''
                SELECT d.*
                FROM patient_record pr JOIN doctor d ON d.id = pr.doctor_id
                WHERE patient_id = %s
                ORDER BY id DESC
                LIMIT 1
                ''',
                (user_id)
            )
            latest_record = cursor.fetchone()

        else:
            return jsonify({'error': 'Invalid role'}), 400
        
        return jsonify({'data': latest_record}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()




#GET ALL PATIENT RECORD HISTORY - PATIENT
def get_records_history(account_id):
    cursor = db.cursor(DictCursor)

    try:
        cursor.execute("""
            SELECT 
                COALESCE(d.id, p.id) AS user_id,
                CASE 
                    WHEN d.id IS NOT NULL THEN 'doctor'
                    WHEN p.id IS NOT NULL THEN 'patient'
                END AS role
            FROM account a
            LEFT JOIN doctor d ON d.account_id = a.id
            LEFT JOIN patient p ON p.account_id = a.id
            WHERE a.id = %s
        """, (account_id,))
        result = cursor.fetchone()

        if not result:
            return jsonify({"error": "Account not found"}), 404

        user_id, role = result['user_id'], result['role']

        if role == 'patient':
            cursor.execute("""
                SELECT * 
                FROM patient_record 
                WHERE patient_id = %s
            """, (user_id))
            history = cursor.fetchall()

        else:
            return jsonify({"error": "Invalid role"}), 400

        # Trả về kết quả
        return jsonify({
            "history": history
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
