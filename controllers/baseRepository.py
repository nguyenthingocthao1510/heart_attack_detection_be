from config.dbconfig.app import db
from utils.logger import Logger

class BaseRepository:
    def __init__(self, db_table):
        self.db_table = db_table
        self.db = db
        self.logger = Logger()

    def _get_cursor(self):
        return self.db.cursor()

    def update(self, set: str, where: str, params):
        cur = self._get_cursor()
        cur.execute(f'UPDATE {self.db_table} SET {set} WHERE {where}', params)
        self.db.commit()
