from config.dbconfig.app import db
from flask import request
from utils.logger import Logger

class BaseRepository:
    def __init__(self, db_table):
        self.db_table = db_table
        self.db = db
        self.logger = Logger()

    def _get_cursor(self):
        return self.db.cursor()

    def get_all(self, select_clause, from_clause, where_clause='', process_func=None):
        cur = self._get_cursor()
        try:
            cur.execute(f'SELECT {select_clause} FROM {from_clause} WHERE {where_clause}')
            datas = cur.fetchall()
            if process_func:
                return [process_func(data) for data in datas]
            return process_func
        except Exception as e:
            self.db.rollback()
            return []
        finally:
            cur.close()
    
    def add(self, columns: str, values: str, params: tuple, where=''):
        cur = self._get_cursor()
        try:
            cur.execute(f'''
                            INSERT INTO {self.db_table}{columns} 
                            VALUES {values}
                            {where}
                        ''', params)
            self.db.commit()
            return {"Successfully stored/added value!"}, 200
        except Exception as e:
            self.db.rollback()
            return e
        finally:
            cur.close()

    def update(self, set: str, where: str, params: tuple):
        cur = self._get_cursor()
        try:
            cur.execute(f'UPDATE {self.db_table} SET {set} WHERE {where}', params)
            self.db.commit()
            return {"Successfully update value!"}, 200
        except Exception as e:
            self.db.rollback()
            return e
        finally:
            cur.close()

    
