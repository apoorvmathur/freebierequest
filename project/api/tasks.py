#import psycopg2 as ps2
import MySQLdb as sql
import random

connection = None

class tasks:
    def getDBCursor():
        global connection
        if (connection == None) or (connection.closed == 0):
            #connection = ps2.connect(dbname="testdb", user="postgres", password="apoorvmathur", host="127.0.0.1", port=5432)
            connection = sql.connect(user="root", password="root", host="127.0.0.1", port=3306)
            connection.autocommit(True)
        cursor = connection.cursor()
        return cursor

    def generateToken(user):
        token = '%030x' % random.randrange(16**30)
        cursor = tasks.getDBCursor()
        cursor.execute("INSERT INTO Freebie.Sessions VALUES (%(token)s, %(username)s) ON DUPLICATE KEY UPDATE token = %(token)s",
                       {"token":token, "username":user})
        cursor.close()
        return token
