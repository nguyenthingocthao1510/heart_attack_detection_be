from flask import request
from config.dbconfig.app import db

#GET ALL 
def get_all():
    cur = db.cursor()
    try:
        cur.execute('SELECT * FROM role')
        roles = cur.fetchall()
        result = []
        for r in roles:
            result.append({
                'id': r[0],
                'name': r[1]
            })
        return {'data': result}, 200
    except Exception as e:
            print(f'Error: {str(e)}')
            return (f'Error: {str(e)}')
    finally:
            cur.close()

#GET BY ID
def get_by_id(id):
      cur = db.cursor()
      try:
            cur.execute('SELECT * FROM role WHERE id = %s', (id,))
            role = cur.fetchone()

            if role:
                  res = {
                        'id': role[0],
                        'name': role[1]
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

            cur = db.cursor()
            try:
                  cur.execute('INSERT INTO role(name) VALUES (%s)', (name))
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
            cur.execute('UPDATE role SET name = %s WHERE id = %s', (name,id))
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
                  cur.execute('DELETE FROM role WHERE id = %s', (id))
                  if cur.rowcount > 0:
                    return {'message': 'Delete successfully'}, 200
                  else:
                       return {'error' : 'Patient ID not found'}, 404
            except Exception as e:
                 db.rollback()
                 return {'error' : str(e)}, 500
            finally:
                cur.close()
                   
