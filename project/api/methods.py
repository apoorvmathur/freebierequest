from project.api.tasks import tasks

class methods:
    def authenticate(user, password):
        cursor = tasks.getDBCursor()
        cursor.execute("SELECT * FROM freebie.Users WHERE username = %(username)s", {"username":user})
        result = cursor.fetchone()
        cursor.close()
        if result:
            if result[1] == password:
                return True
        return False

    def verify(user, token):
        cursor = tasks.getDBCursor()
        cursor.execute("SELECT * FROM freebie.Sessions where username = %(username)s", {"username":user})
        result = cursor.fetchone()
        cursor.close()
        if result:
            if result[0] == token:
                return True
        return False
