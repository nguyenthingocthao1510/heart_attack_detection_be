from config.dbconfig.app import db
from utils.logger import Logger

class BaseRepository:
    def __init__(self, db_table):
        self.db_table = db_table
        self.db = db
        self.logger = Logger()

    def _get_cursor(self):
        return self.db.cursor()
    
    def add(self, columns: str, values: str, params: tuple, where_claus=''):
        cur = self._get_cursor()
        try:
            cur.execute(f'''
                            INSERT INTO {self.db_table}{columns} 
                            VALUES {values}
                            {where_claus}
                        ''', params)
            self.db.commit()
            self.logger.info('"Successfully stored diagnosis history"')
            return {"Successfully stored diagnosis history"}, 200
        except Exception as e:
            self.db.rollback()
            self.logger.error(f'An error occurred: {e}')
            return e
        finally:
            cur.close()

    def update(self, set: str, where: str, params: tuple):
        cur = self._get_cursor()
        cur.execute(f'UPDATE {self.db_table} SET {set} WHERE {where}', params)
        self.db.commit()

    
