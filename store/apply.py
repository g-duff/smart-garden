import sqlite3

DATABASE_FILE = 'garden.db'
MIGRATION_SCRIPT = 'v0.sql'

with open(MIGRATION_SCRIPT, 'r') as sql_file:
    sql_script = sql_file.read()

db = sqlite3.connect(DATABASE_FILE)
cursor = db.cursor()
cursor.executescript(sql_script)
db.commit()
db.close()
