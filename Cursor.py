import sqlite3

class Cursor:
    def __init__(self, db, dictmode=False):
        self.connection = sqlite3.connect(db)
        if dictmode:
            self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()
    
    def __enter__(self):
        return self.cursor
    
    def __exit__(self, ext_type, exc_value, traceback):
        self.cursor.close()
        if isinstance(exc_value, Exception):
            self.connection.rollback()
        else:
            self.connection.commit()
        self.connection.close()
    
    def __iter__(self):
        for i in self.cursor:
            yield i