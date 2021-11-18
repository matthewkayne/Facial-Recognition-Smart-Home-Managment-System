
import sqlite3

# define connection and cursor

connection = sqlite3.connect('accounts.db')
cursor = connection.cursor()

# create stores table

command1 = """CREATE TABLE IF NOT EXISTS
accounts(id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT)"""

cursor.execute(command1)


connection.commit()

def addAccount(mainName,mainPass):
    cursor.execute("INSERT INTO accounts (username, password) VALUES (?, ?)",(mainName,mainPass))
    connection.commit()


def cleanTable(tableName):
    cursor.execute("DELETE FROM "+tableName)
    connection.commit()

