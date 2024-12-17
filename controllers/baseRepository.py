from config.dbconfig.app import db

class BaseRepository:
    def __init__(self, db_table):
        self.db_table = db_table
        self.cur = db.cursor()