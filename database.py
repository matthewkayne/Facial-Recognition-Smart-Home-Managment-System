import sqlite3

# define connection and cursor

connection = sqlite3.connect('accounts.db')
cursor = connection.cursor()

# create stores table

command1 = """CREATE TABLE IF NOT EXISTS
accounts(id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT, filename TEXT)"""

cursor.execute(command1)


connection.commit()

def addAccount(mainName,mainPass,mainFileName):
    cursor.execute("INSERT INTO accounts (username, password, filename) VALUES (?, ?, ?)",(mainName,mainPass,mainFileName))
    connection.commit()

#Emptys out entire table
def cleanTable(tableName):
    cursor.execute("DELETE FROM "+tableName)
    connection.commit()
#cleanTable("accounts")

