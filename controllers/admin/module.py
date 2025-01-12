from flask import request, jsonify
from config.dbconfig.app import db

# GET ALL 
def get_all():
    cur = db.cursor()
    try:
        cur.execute('SELECT * FROM module')
        modules = cur.fetchall()
        result = []
        for m in modules:
            result.append({
                'id': m[0],
                'name': m[1],
                'route': m[2],
                'image': m[3],
            })
        return jsonify({'data': result})
    except Exception as e:
            print(f"Error occurred: {str(e)}")
            return jsonify({'error': str(e)}), 500
    finally:
            cur.close()

def get_for_list():
    if request.method == 'POST':
        cursor = db.cursor()
        data = request.json
        name = data.get('name')

        try:
            cursor.execute("SELECT * FROM module WHERE name LIKE %s", (f"%{name}%",))
            modules = cursor.fetchall()

            result = []
            for m in modules:
                result.append({
                    'id': m[0],
                    'name': m[1],
                    'route': m[2],
                    'image': m[3],
                })

            return jsonify({'data': result})

        except Exception as e:
            print(f"Error occurred: {str(e)}")
            return jsonify({'error': str(e)}), 500

        finally:
            cursor.close()

#GET BY ID
def get_by_id(id):
      cur = db.cursor()
      try:
            cur.execute('SELECT * FROM module WHERE id = %s', (id,))
            module = cur.fetchone()

            if module:
                  res = {
                        'id': module[0],
                        'name': module[1],
                        'route': module[2],
                        'image': module[3],
                  }
                  return {'data': res}, 200
            else:
                  return {'error':'Patient not found'}, 404
      except Exception as e:
            print(f'Error: {str(e)}')
            return (f'Error: {str(e)}')
      finally:
            cur.close()

#INSERT
def add():
    if request.method == 'POST':
        data = request.get_json()
        name = data['name']
        route = data['route']
        image = data['image']

        cur = db.cursor()
        try:
            cur.execute('INSERT INTO module(name, route, image) VALUES (%s,%s,%s)', (name, route, image))
            db.commit()
            return {'data': data}, 200
        except Exception as e:
            db.rollback()
            return (f'Error: {str(e)}')
        finally:
            cur.close()

#UPDATE
def update(id):
    if request.method == 'PUT':
        data = request.get_json()
        if not data:
            return {'error': 'No JSON payload received'}, 400

        update_fields = []
        update_values = []

        if 'name' in data:
            update_fields.append("name = %s")
            update_values.append(data['name'])

        if 'route' in data:
            update_fields.append("route = %s")
            update_values.append(data['route'])

        if 'image' in data:
            update_fields.append("image = %s")
            update_values.append(data['image'])

        if not update_fields:
            return {'error': 'No fields provided to update'}, 400

        update_values.append(id)

        update_query = f"UPDATE module SET {', '.join(update_fields)} WHERE id = %s"

        cur = db.cursor()

        try:
            cur.execute(update_query, tuple(update_values))
            if cur.rowcount > 0:
                return {'message': 'Module updated successfully'}, 200
            else:
                return {'error': 'ID not found'}, 404
        except Exception as e:
            db.rollback()
            return {'error': f'Error: {str(e)}'}, 500
        finally:
            cur.close()


#DELETE
def delete(id):
      if request.method == 'DELETE':
            cur = db.cursor()        
            try:
                  cur.execute('DELETE FROM module WHERE id = %s', (id))
                  if cur.rowcount > 0:
                    return {'message': 'Delete successfully'}, 200
                  else:
                       return {'error' : 'Module ID not found'}, 404
            except Exception as e:
                 db.rollback()
                 return {'error' : str(e)}, 500
            finally:
                cur.close()
                   
