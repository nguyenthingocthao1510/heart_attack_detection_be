from flask import request, jsonify
from dbconfig.app import db

#GET ALL 
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
      name = data['name']

      cur = db.cursor()

      try:
            cur.execute('UPDATE module SET name = %s WHERE id = %s', (name,id))
            if cur.rowcount > 0:
                  return {'data': data}, 200
            else:
                return ('ID not found', 404) 
      except Exception as e:
            db.rollback()
            return (f'Error: {str(e)}', 500) 
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
                   
