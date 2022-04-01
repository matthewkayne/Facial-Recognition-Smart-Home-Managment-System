import sqlite3

connection = sqlite3.connect('database.db') # Define connection and cursor
cursor = connection.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS
accounts(id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT, email TEXT,filename TEXT)""") # Create accounts table

cursor.execute("""CREATE TABLE IF NOT EXISTS
devices(id INTEGER PRIMARY KEY AUTOINCREMENT, devicename TEXT)""") # Create devices table



cursor.execute("""CREATE TABLE IF NOT EXISTS
link(id INTEGER PRIMARY KEY AUTOINCREMENT, userid INTEGER, deviceid INTEGER, state INTEGER DEFAULT 0, FOREIGN KEY(userid) REFERENCES accounts(id), FOREIGN KEY(deviceid) REFERENCES devices(id))""") # Create link table


def addAccount(mainName,mainPass,mainEmail,mainFileName): # Adds new row to accounts table
    cursor.execute("INSERT INTO accounts (username, password, email, filename) VALUES (?, ?, ?, ?)",(mainName,mainPass,mainEmail,mainFileName))
    connection.commit()


def addDevice(deviceName): # Adds new row to devices table
    cursor.execute("INSERT INTO devices (devicename) VALUES (?)",(deviceName,))
    connection.commit()

def createTestTable():
    cursor.execute("""CREATE TABLE IF NOT EXISTS test(id INTEGER PRIMARY KEY AUTOINCREMENT, devicename TEXT)""")
    connection.commit()
    
def deleteTestTable():
    cursor.execute("DROP TABLE IF EXISTS test")
    connection.commit()
