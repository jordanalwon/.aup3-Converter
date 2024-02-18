import sqlite3

class SQLite3Reader():
    def __init__(self, path):
        connection = sqlite3.connect(path)
        self.cursor = connection.cursor()

    def binary_name_space(self):
        return self.cursor.execute("SELECT dict from project;").fetchall()[0][0]
    
    def binary_xml(self):
        return self.cursor.execute("SELECT doc from project;").fetchall()[0][0]

    def binary_sammpleblock(self, id):
        return self.cursor.execute(f"SELECT samples from sampleblocks WHERE blockid={id};").fetchone()[0]