import sqlite3

# define connection and cursor

connection = sqlite3.connect('accounts.db')
cursor = connection.cursor()

# create stores table

command1 = """CREATE TABLE IF NOT EXISTS
accounts(id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT)"""

cursor.execute(command1)

cursor.execute("""INSERT INTO accounts (username, password) VALUES ("matthew", "shhh")""")

connection.commit()


def cleanTable(tableName):
    cursor.execute("DELETE FROM "+tableName)
    connection.commit()