import sqlite3

# Define connection and cursor
connection = sqlite3.connect('database.db')
cursor = connection.cursor()

# Create accounts table
cursor.execute("""CREATE TABLE IF NOT EXISTS
accounts(id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT, filename TEXT)""")

# Create device table
cursor.execute("""CREATE TABLE IF NOT EXISTS
devices(id INTEGER PRIMARY KEY AUTOINCREMENT, devicename TEXT, url TEXT)""")

# Create link table
cursor.execute("""CREATE TABLE IF NOT EXISTS
link(id INTEGER PRIMARY KEY AUTOINCREMENT, userid INTEGER, deviceid INTEGER, state INTEGER DEFAULT 0, FOREIGN KEY(userid) REFERENCES accounts(id), FOREIGN KEY(deviceid) REFERENCES devices(id))""")

connection.commit()

def addAccount(mainName,mainPass,mainFileName):
    cursor.execute("INSERT INTO accounts (username, password, filename) VALUES (?, ?, ?)",(mainName,mainPass,mainFileName))
    connection.commit()

# Emptys out entire table
def cleanTable(tableName):
    cursor.execute("DELETE FROM "+tableName)
    connection.commit()