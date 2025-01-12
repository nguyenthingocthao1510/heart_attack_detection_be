from flask import request, jsonify
from config.dbconfig.app import db

def get_all(account_id):
    cur = db.cursor()
    try:
        cur.execute('''SELECT DISTINCT
                    p.id AS prescription_id,
                    d.name AS doctor_name,
                    pa.name AS patient_name,
                    p.prescription_date,
                    d.id as doctor_id
                    FROM prescription p
                    JOIN patient pa ON p.patient_id = pa.id
                    JOIN doctor d ON p.doctor_id = d.id
                    WHERE d.account_id = %s''', (account_id,))
        
        prescriptions = cur.fetchall()
        result = []
        for p in prescriptions:
            result.append({
                'prescription_id': p[0],        
                'doctor_name': p[1],
                'patient_name': p[2],
                'prescription_date': p[3],
                'doctor_id': p[4]
            })
        
        return jsonify({'data': result}), 200

    except Exception as e:
        print(f'Error: {str(e)}')
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()

def get_for_list():
    if request.method == 'POST':
        cursor = db.cursor()
        data = request.json
        patient_name = data.get('patient_name')
        account_id = data.get('account_id')
        
        try:
            cursor.execute("""SELECT DISTINCT
                    p.id AS prescription_id,
                    d.name AS doctor_name,
                    pa.name AS patient_name,
                    p.prescription_date,
                    d.id as doctor_id
                    FROM prescription p
                    JOIN patient pa ON p.patient_id = pa.id
                    JOIN doctor d ON p.doctor_id = d.id
                    WHERE d.account_id = % s AND pa.name LIKE %s""",((account_id, f"%{patient_name}%",)))
            prescriptions = cursor.fetchall()

            result = []
            for p in prescriptions:
                 result.append({
                'prescription_id': p[0],        
                'doctor_name': p[1],
                'patient_name': p[2],
                'prescription_date': p[3],
                'doctor_id': p[4]
            })
            return jsonify({'data': result})

        except Exception as e:
            print(f"Error occurred: {str(e)}")
            return jsonify({'error': str(e)}), 500

        finally:
            cursor.close()

def get_by_id(account_id, prescription_id):
    cur = db.cursor()
    try:
        cur.execute('''
            SELECT 
                p.id AS prescription_id,
                pa.id AS patient_id,
                pa.name AS patient_name,
                d.name AS doctor_name,
                p.prescription_date,
                p.note,
                pd.id AS prescription_detail_id,
                pd.medicine_amount,
                pd.usage_instructions,
                m.id AS medicine_id,  
                d.account_id
            FROM prescription p
            JOIN patient pa ON p.patient_id = pa.id
            JOIN doctor d ON p.doctor_id = d.id
            JOIN prescription_details pd ON p.id = pd.prescription_id
            JOIN medicine m ON pd.medicine_id = m.id
            WHERE d.account_id = %s AND p.id = %s
        ''', (account_id, prescription_id))

        results = cur.fetchall()
        if not results:
            return jsonify({'error': 'Prescription not found'}), 404

        prescription_data = None
        details = []

        for row in results:
            if not prescription_data:
                prescription_data = {
                    'prescription_id': row[0],
                    'patient_id': row[1],
                    'patient_name': row[2],
                    'doctor_name': row[3],
                    'prescription_date': row[4],
                    'note': row[5],
                    'details': details,  # Link the details
                }
            details.append({
                'id': row[6],  # prescription_detail_id
                'medicine_amount': row[7],  # medicine_id now included
                'usage_instructions': row[8],  # medicine_amount
                'medicine_id': row[9],  # usage_instructions
            })

        return jsonify({'data': prescription_data}), 200

    except Exception as e:
        print(f'Error: {str(e)}')
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()


def create_prescription():
    if request.method == 'POST':
        data = request.json
        cur = db.cursor()
        try:
            patient_id = data['patient_id']
            prescription_date = data['prescription_date']
            doctor_id = data['doctor_id']
            note = data['note']

            prescription_query = '''
                INSERT INTO prescription (patient_id, prescription_date, doctor_id, note)
                VALUES (%s, %s, %s, %s)
            '''
            cur.execute(prescription_query, (patient_id, prescription_date, doctor_id, note))
            prescription_id = cur.lastrowid  
            
            details = data['details']
            for detail in details:
                medicine_id = detail['medicine_id']
                medicine_amount = detail['medicine_amount']
                usage_instructions = detail['usage_instructions']

                detail_query = '''
                    INSERT INTO prescription_details (prescription_id, medicine_id, medicine_amount, usage_instructions)
                    VALUES (%s, %s, %s, %s)
                '''
                cur.execute(detail_query, (prescription_id, medicine_id, medicine_amount, usage_instructions))

            db.commit()  
            
            return jsonify({
                'message': 'Prescription created successfully',
                'prescription_id': prescription_id,
            }), 200
        except Exception as e:
            db.rollback()
            print(f"Error: {str(e)}")
            return jsonify({'error': str(e)}), 500

def update_prescription_detail(prescription_id):
    if request.method == 'PUT':
        data = request.json
        cur = db.cursor()
        try:
            details = data.get('details', [])
            
            if not details:
                return jsonify({'error': 'No details provided'}), 400
            
            for detail in details:
                prescription_detail_id = detail.get('id')  
                medicine_id = detail.get('medicine_id')
                medicine_amount = detail.get('medicine_amount')
                usage_instructions = detail.get('usage_instructions')

                # Ensure all necessary fields are provided
                if prescription_detail_id is None or medicine_id is None or medicine_amount is None or usage_instructions is None:
                    return jsonify({'error': 'Missing required fields'}), 400

                # Log for debugging
                print(f"Updating detail with prescription_detail_id: {prescription_detail_id} for prescription_id: {prescription_id}")

                # Execute the update
                cur.execute('''
                    UPDATE prescription_details 
                    SET medicine_id = %s, medicine_amount = %s, usage_instructions = %s 
                    WHERE id = %s AND prescription_id = %s
                ''', (medicine_id, medicine_amount, usage_instructions, prescription_detail_id, prescription_id))
                
                # Check if the row was updated
                print(f"Rows affected: {cur.rowcount}")
                
            # Commit the changes
            db.commit()  

            return jsonify({'message': 'Prescription details updated successfully'}), 200

        except Exception as e:
            print(f"Error occurred: {str(e)}")  # Log the error
            db.rollback()  
            return jsonify({'error': str(e)}), 500

        
def delete(id):
    if request.method == 'DELETE':
        cur = db.cursor()
        try:
            cur.execute('DELETE FROM prescription_details WHERE prescription_id = %s', (id,))
            
            cur.execute('DELETE FROM prescription WHERE id = %s', (id,))
            
            if cur.rowcount > 0:
                db.commit()  
                return {'message': 'Delete successfully'}, 200
            else:
                return {'error': 'Prescription ID not found'}, 404
        except Exception as e:
            db.rollback()  
            return {'error': str(e)}, 500

def patient_get_all(patient_id):
    cur = db.cursor()
    try:
        cur.execute('''
SELECT p.id as prescription_id,
       p.patient_id,
       p.prescription_date,
       p.doctor_id,
       p.note,
       pd.medicine_id,
       pd.medicine_amount,
       pd.usage_instructions
FROM prescription p 
JOIN prescription_details pd 
ON p.id = pd.prescription_id
WHERE p.patient_id = %s
''', (patient_id,))
        prescriptions = cur.fetchall()
        result = []
        for p in prescriptions:
            result.append({
                'prescription_id': p[0],
                'patient_id': p[1],
                'prescription_date': p[2],
                'doctor_id': p[3],
                'note': p[4],
                'medicine_id': p[5],
                'medicine_amount': p[6],
                'usage_instructions': p[7],
            })
        return jsonify({'data': result}), 200
    except Exception as e:
        print(f'Error: {str(e)}')
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()

def get_all_doctor():
    cur = db.cursor()
    result = []
    try:
        cur.execute('SELECT id, name FROM doctor')
        doctors = cur.fetchall()
        for d in doctors:
            result.append({
                'id': d[0],
                'name': d[1]
            })
        return jsonify({'data': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()

def get_all_medicine():
    cur = db.cursor()
    result = []
    try:
        cur.execute('SELECT id, name FROM medicine')
        doctors = cur.fetchall()
        for d in doctors:
            result.append({
                'id': d[0],
                'name': d[1]
            })
        return jsonify({'data': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()



