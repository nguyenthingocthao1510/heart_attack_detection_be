from flask import request, Response, jsonify
from utils.utils import generate_salt,generate_hash,generate_jwt_token, db_write, db_read, validate_user
from dbconfig.app import db

#REGISTER
def register():
    user_username = request.json['username']
    user_password = request.json['password']
    user_role = request.json['role_id']

    password_salt = generate_salt()
    password_hash = generate_hash(user_password, password_salt)

    try:
        if db_write('''INSERT INTO account(username, password_salt, password_hash, role_id) VALUES (%s,%s,%s,%s)''', (user_username,password_salt, password_hash ,user_role)):
            return Response(status=201)
    except Exception as e:
        print('Error: ', str(e))
        return Response(status=409)

def login():
    user_username = request.json['username']
    user_password = request.json['password']

    user_token = validate_user(user_username, user_password)

    if user_token:
        return jsonify({
            'message': 'Login successfully',
            'jwt_token': user_token['jwt_token'],  
            'roleId': user_token['role_id'],
            'accountId': user_token['id']       
        })
    else:
        return Response(status=401) 


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