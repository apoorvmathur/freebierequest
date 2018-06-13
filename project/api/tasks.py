import psycopg2 as ps2
import random

connection = None

class tasks:
    def getDBCursor():
        global connection
        if (connection == None) or (connection.closed == 0):
            connection = ps2.connect(dbname="testdb", user="postgres", password="apoorvmathur", host="127.0.0.1", port=5432)
            connection.autocommit = True
        cursor = connection.cursor()
        return cursor

    def generateToken(user):
        token = '%030x' % random.randrange(16**30)
        cursor = tasks.getDBCursor()
        cursor.execute("INSERT INTO freebie.sessions VALUES (%s, %s) ON CONFLICT (username) DO UPDATE SET token = Excluded.token", (token, user))
        cursor.close()
        return token
