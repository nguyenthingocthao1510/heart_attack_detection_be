from flask import request, Response, jsonify
from utils.utils import generate_salt,generate_hash,generate_jwt_token, db_write, db_read, validate_user
from config.dbconfig.app import db

#REGISTER
def register():
    user_username = request.json['username']
    user_password = request.json['password']
    user_role = request.json['role_id']
    user_status = 'Active'

    password_salt = generate_salt()
    password_hash = generate_hash(user_password, password_salt)

    try:
        if db_write('''INSERT INTO account(username, password_salt, password_hash, role_id, account_status) VALUES (%s,%s,%s,%s,%s)''', (user_username,password_salt, password_hash ,user_role, user_status)):
            return Response(status=200)
    except Exception as e:
        print('Error: ', str(e))
        return Response(status=409)

def update_password(account_id):
    try:
        user_password = request.json.get('user_password', '').strip()
        if not user_password or len(user_password) < 1:
            return {"message": "Password must be at least 1 characters long"}, 400

        password_salt = generate_salt()
        password_hash = generate_hash(user_password, password_salt)
        account_status = request.json.get('account_status')

        query = '''
        UPDATE account 
        SET password_salt = %s, password_hash = %s , account_status = %s
        WHERE id = %s
        '''
        if db_write(query, (password_salt, password_hash, account_status, account_id)):
            return {"message": "Password updated successfully"}, 200
        else:
            return {"message": "Failed to update password"}, 500

    except Exception as e:
        print('Error: ', str(e))
        return {"message": "An error occurred while updating password"}, 500

def login():
    user_username = request.json['username']
    user_password = request.json['password']

    user_token = validate_user(user_username, user_password)

    if user_token:
        cur = db.cursor()
        try: 
            cur.execute('UPDATE account SET account_status = %s WHERE id = %s', ('Active', user_token['id']))
            db.commit()
        except Exception as e:
            return (f'Error: {str(e)}')
        finally:
            cur.close()

        return jsonify({
            'message': 'Login successfully',
            'jwt_token': user_token['jwt_token'],  
            'roleId': user_token['role_id'],
            'accountId': user_token['id']
        })
    else:
        return Response(status=401) 
    
def logout(account_id):
    cur = db.cursor()
    try: 
        cur.execute('UPDATE account SET account_status = %s WHERE id = %s', ('Inactive', account_id))
        db.commit()
    except Exception as e:
        return (f'Error: {str(e)}')
    finally:
        cur.close()

def get_active_user():
    cur = db.cursor()
    try: 
        cur.execute('SELECT * FROM account WHERE account_status = %s', 'Active')
        accounts = cur.fetchall()
        result = []
        for a in accounts:
            result.append({
                'id': a[0],
            })
        return {
            'data': result
        }
    except Exception as e:
        return (f'Error: {str(e)}')
    finally:
        cur.close()

def get_all():
    cur = db.cursor()
    try:
        cur.execute('SELECT * FROM account')
        accounts = cur.fetchall()
        result = []
        for a in accounts:
            result.append({
                'id': a[0],
                'username': a[1],
                'account_status': a[6],
            })
        return jsonify({'data': result})
    except Exception as e:
            return (f'Error: {str(e)}')
    finally:
        cur.close()

def get_account_on_role(account_id):
    cur = db.cursor()
    try:
        cur.execute('SELECT r.name, r.id FROM role r JOIN account a ON r.id = a.role_id WHERE a.id = %s', (account_id))
        account_role = cur.fetchone()

        if account_role:
            res = {
                'name' : account_role[0],
                'id': account_role[1],
            }
            return {'data': res}, 200
        else:
            return {'error':'Account not found'}, 404
    except Exception as e:
        return (f'Error: {str(e)}')
    finally:
        cur.close()