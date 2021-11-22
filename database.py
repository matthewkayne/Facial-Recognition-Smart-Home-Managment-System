import sqlite3

# define connection and cursor
connection = sqlite3.connect('database.db')
cursor = connection.cursor()

# create accounts table
cursor.execute("""CREATE TABLE IF NOT EXISTS
accounts(id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT, filename TEXT)""")

# create device table
cursor.execute("""CREATE TABLE IF NOT EXISTS
devices(id INTEGER PRIMARY KEY AUTOINCREMENT, devicename TEXT, url TEXT)""")

# create link table
cursor.execute("""CREATE TABLE IF NOT EXISTS
link(id INTEGER PRIMARY KEY AUTOINCREMENT, userid INTEGER, deviceid INTEGER, state INTEGER DEFAULT 0, FOREIGN KEY(userid) REFERENCES accounts(id), FOREIGN KEY(deviceid) REFERENCES devices(id))""")
# use most recent record or the same userId and deviceId combination


connection.commit()

def addAccount(mainName,mainPass,mainFileName):
    cursor.execute("INSERT INTO accounts (username, password, filename) VALUES (?, ?, ?)",(mainName,mainPass,mainFileName))
    connection.commit()

# Emptys out entire table
def cleanTable(tableName):
    cursor.execute("DELETE FROM "+tableName)
    connection.commit()  