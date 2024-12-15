from config.dbconfig.app import db
from flask import request, jsonify

def get_all_permission_in_role_module(role_id, module_id):
    if request.method == 'GET':
        cur = db.cursor()
        try:
            cur.execute('SELECT COUNT(*) FROM role WHERE id = %s', (role_id,))
            if cur.fetchone()[0] == 0:
                return jsonify({'Error': 'roleId not found'}), 404

            cur.execute('SELECT COUNT(*) FROM module WHERE id = %s', (module_id,))
            if cur.fetchone()[0] == 0:
                return jsonify({'Error': 'moduleId not found'}), 404

            cur.execute('SELECT p.id, p.name FROM permission p JOIN module_role_permission mrp ON p.id = mrp.permission_id WHERE mrp.role_id = %s AND mrp.module_id = %s', (role_id, module_id))
            permission_module_role = cur.fetchall()
            result = []
            for pmr in permission_module_role:
                result.append({
                    'id': pmr[0],
                    'name': pmr[1],
                })
            return jsonify({'data': result}), 200
        except Exception as e:
            return jsonify({'Error': str(e)}), 500
        finally:
            cur.close()

def get_all_permission_not_in_role_module(role_id, module_id):
    if request.method == 'GET':
        cur = db.cursor()
        try:
            cur.execute('SELECT COUNT(*) FROM role WHERE id = %s', (role_id,))
            if cur.fetchone()[0] == 0:
                return jsonify({'Error': 'roleId not found'}), 404

            cur.execute('SELECT COUNT(*) FROM module WHERE id = %s', (module_id,))
            if cur.fetchone()[0] == 0:
                return jsonify({'Error': 'moduleId not found'}), 404

            cur.execute('SELECT p.id, p.name FROM permission p WHERE p.id NOT IN ( SELECT mrp.permission_id FROM module_role_permission mrp WHERE mrp.role_id = %s AND mrp.module_id = %s );', (role_id, module_id))
            permission_module_role = cur.fetchall()
            result = []
            for pmr in permission_module_role:
                result.append({
                    'id': pmr[0],
                    'name': pmr[1],
                })
            return jsonify({'data': result}), 200
        except Exception as e:
            return jsonify({'Error': str(e)}), 500
        finally:
            cur.close()

def insert_permission_into_role_module(module_id, role_id, permission_ids):
    cur = db.cursor()
    sql = 'INSERT INTO module_role_permission (module_id, role_id, permission_id) VALUES (%s, %s, %s)'
    values = [(module_id, role_id, permission_id) for permission_id in permission_ids]
    try:
        cur.executemany(sql, values)  
        db.commit()  
        return jsonify({'message': 'Insert success'})
    except Exception as e:
        db.rollback()  
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()

def delete_permission_into_role_module(module_id, role_id, permission_ids):
    permission_ids_tuple = tuple(permission_ids)
    sql = f'DELETE FROM module_role_permission WHERE role_id = %s AND module_id = %s AND permission_id IN ({",".join(["%s"] * len(permission_ids))})'
    cur = db.cursor()

    try:
        cur.execute(sql, (role_id, module_id) + permission_ids_tuple)
        db.commit()
        return {'message': 'Deleted success'}
    except Exception as e:
        db.rollback()
        return {'error': str(e)}
    finally:
        cur.close()

def load_all_permission_information(role_id):
    cur = db.cursor()
    sql = 'SELECT p.id, m.name as module_name, p.name, mrp.role_id FROM permission p JOIN module_role_permission mrp ON p.id = mrp.permission_id JOIN module m ON m.id = mrp.module_id WHERE mrp.role_id = %s'

    try:
        cur.execute(sql, (role_id,))
        result = cur.fetchall()

        data = {
            'roleId': role_id,
            'permission': {}
        }

        for row in result:
            module_name = row[1]
            permission_name = row[2]

            if module_name not in data['permission']:
                data['permission'][module_name] = []
            data['permission'][module_name].append(permission_name)
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'Error': str(e)}),500
    finally:
        cur.close()





