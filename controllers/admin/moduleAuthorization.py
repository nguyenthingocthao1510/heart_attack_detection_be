from dbconfig.app import db
from flask import request, jsonify

def get_module_in_role(role_id):
    if request.method == 'GET':
        cur = db.cursor()
        try:
            cur.execute('SELECT * FROM module WHERE id IN(SELECT module_id FROM module_role WHERE role_id=%s)', (role_id))
            module_roles = cur.fetchall()
            result = []
            for mr in module_roles:
                result.append({
                    'id': mr[0],
                    'name': mr[1],
                    'route': mr[2],
                    'image': mr[3]
                })
            return jsonify({'data': result}), 200
        except Exception as e:
            return jsonify({'Error': str(e)}), 500
        finally:
            cur.close

def get_module_not_in_role(role_id):
    if request.method == 'GET':
        cur = db.cursor()
        try:
            cur.execute('SELECT * FROM module WHERE id NOT IN (SELECT module_id FROM module_role WHERE role_id = %s)', (role_id))
            module_roles = cur.fetchall()
            result = []
            for mr in module_roles:
                result.append({
                    'id': mr[0],
                    'name': mr[1],
                    'route': mr[2],
                    'image': mr[3]
                })
            return jsonify({'data' : result}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        finally:
            cur.close()

def add_module_into_role(role_id, module_ids):
    cur = db.cursor()
    sql = 'INSERT INTO module_role (module_id, role_id) VALUES (%s, %s)'
    values = [(module_id, role_id) for module_id in module_ids]
    
    try:
        cur.executemany(sql, values)
        db.commit()
        return jsonify({'message': f'Inserted success'})
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()
        
def delete_module_in_role(role_id, module_ids):
    module_ids_tuple = tuple(module_ids)
    sql = f'DELETE FROM module_role WHERE role_id = %s AND module_id IN {module_ids_tuple}'
    cur = db.cursor()

    try:
        cur.execute(sql, (role_id,))
        db.commit()
        return {'message': f'Deleted success'}
    except Exception as e:
        db.rollback()
        return {'error': str(e)}
    finally:
        cur.close()


