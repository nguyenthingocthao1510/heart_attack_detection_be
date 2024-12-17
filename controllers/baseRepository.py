from config.dbconfig.app import db
from utils.logger import Logger

class BaseRepository:
    def __init__(self, db_table, logger):
        self.db_table = db_table
        self.cur = db.cursor()
        self.db = db
        self.logger = Logger(logger)