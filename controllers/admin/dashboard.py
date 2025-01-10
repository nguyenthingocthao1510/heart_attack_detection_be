from flask import request, jsonify
from config.dbconfig.app import db

def get_activate_status():
    cursor = db.cursor()
    try:
        cursor.execute('''
            SELECT COUNT(account_status) AS total_amount, 'Active' as name
            FROM account
            WHERE account_status = 'Active';
        ''')
        result = cursor.fetchone()
        if result:
            res = {
                'total_amount': result[0],
                'name': result[1]
            }
            return jsonify({'data': res}), 200
        else:
            return jsonify({'error': 'No account is activated'}), 404
    except Exception as e:
        print(f'error: {str(e)}')
        return jsonify({'error': f'Something went wrong: {str(e)}'}), 500
    finally:
        cursor.close()

def get_deactivate_status():
    cursor = db.cursor()
    try:
        cursor.execute('''
            SELECT COUNT(account_status) AS total_amount, 'Inactive' as name
            FROM account
            WHERE account_status = 'Inactive';
        ''')
        result = cursor.fetchone()
        if result:
            res = {
                'total_amount': result[0],
                'name': result[1]
            }
            return jsonify({'data': res}), 200
        else:
            return jsonify({'error': 'No account is inactive'}), 404
    except Exception as e:
        print(f'error: {str(e)}')
        return jsonify({'error': f'Something went wrong: {str(e)}'}), 500
    finally:
        cursor.close()

def get_assign_status():
    cursor = db.cursor()
    try:
        cursor.execute('''
            SELECT COUNT(id) AS total_amount, 'Assign' AS name
            FROM device
            WHERE patient_id IS NOT NULL;
        ''')
        result = cursor.fetchone()
        if result:
            res = {
                'total_amount': result[0],
                'name': result[1]
            }
            return jsonify({'data': res}), 200
        else:
            return jsonify({'error': 'No devices are assigned to patients'}), 404
    except Exception as e:
        print(f'error: {str(e)}')
        return jsonify({'error': f'Something went wrong: {str(e)}'}), 500
    finally:
        cursor.close()

def get_not_assign_status():
    cursor = db.cursor()
    try:
        cursor.execute('''
            SELECT COUNT(id) AS total_amount, 'Not assign' AS name
            FROM device 
            WHERE patient_id IS NULL;
        ''')
        result = cursor.fetchone()
        if result:
            res = {
                'total_amount': result[0],
                'name': result[1]
            }
            return jsonify({'data': res}), 200
        else:
            return jsonify({'error': 'No devices are unassigned'}), 404
    except Exception as e:
        print(f'error: {str(e)}')
        return jsonify({'error': f'Something went wrong: {str(e)}'}), 500
    finally:
        cursor.close()

def get_medicine_information():
    cursor = db.cursor()
    try:
        query = '''
            SELECT 'Patient' AS name, COUNT(id) AS count FROM patient
            UNION
            SELECT 'Module' AS name, COUNT(id) AS count FROM module
            UNION
            SELECT 'Device' AS name, COUNT(id) AS count FROM device
            UNION
            SELECT 'Medicine' AS name, COUNT(id) AS count FROM medicine
            UNION
            SELECT 'Account' AS name, COUNT(id) AS count FROM account;
        '''
        cursor.execute(query)
        result = cursor.fetchall()
        if result:
            data = [{'name': d[0], 'total_amount': d[1]} for d in result]
            return jsonify({'data': data}), 200
        else:
            return jsonify({'error': 'No data found'}), 404
    except Exception as e:
        print(f'Error: {str(e)}')
        return jsonify({'error': f'Something went wrong: {str(e)}'}), 500
    finally:
        cursor.close()
