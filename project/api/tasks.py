#import psycopg2 as ps2
import MySQLdb as sql
import random

connection = None

class tasks:
    def getDBCursor():
        global connection
        if (connection == None) or (connection.closed == 1):
            #connection = ps2.connect(dbname="testdb", user="postgres", password="apoorvmathur", host="127.0.0.1", port=5432)
            connection = sql.connect(user="biindia", password="299A9052D0E6", host="pms-db.ccee0gkyjvah.ap-southeast-1.rds.amazonaws.com", port=3306)
            connection.autocommit(True)
        cursor = connection.cursor()
        if not(tasks.testCon(cursor)):
            connection.close()
            return tasks.getDBCursor()
        return cursor

    def generateToken(user):
        token = '%030x' % random.randrange(16**30)
        cursor = tasks.getDBCursor()
        cursor.execute("INSERT INTO pms.Freebie_Sessions VALUES (%(token)s, %(username)s) ON DUPLICATE KEY UPDATE token = %(token)s",
                       {"token":token, "username":user})
        cursor.close()
        return token

    def testCon(cursor):
        try:
            cursor.execute("show databases")
            test_result = cursor.fetchall()
            return True
        except cursor.OperationalError as e:
            if (e.args[0] == 2006):
                print("Connection Gaya!")
                return False
            else:
                raise e
