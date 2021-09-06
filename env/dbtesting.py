import sqlite3

con = sqlite3.connect('abroad.db')
cursor = con.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cursor.fetchall())
con.close()