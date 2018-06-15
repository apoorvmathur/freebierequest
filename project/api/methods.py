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

    def convertToJSON(result_set):
        outJSON = []
        for result in result_set:
            row = {
                "id":result[0],
                "agent_name":result[1],
                "category":result[2],
                "account_phone":result[3],
                "sales_date":result[4],
                "activation_date":result[5],
                "sales_amount":result[6],
                "prev_sales":result[7],
                "discount_amount":result[8],
                "discount_percent":float(result[9]),
                "alternate_number":result[10],
                "discussion_details":result[11],
                "status":result[12]
            }
            outJSON.append(row)
        return outJSON

    def getRequests(userId):
        cursor = tasks.getDBCursor()
        cursor.execute("SELECT userlevel FROM Freebie.Users where username = %(username)s", {"username":userId})
        user = cursor.fetchone()
        print(user)
        level = user[0]
        if level == 1:
            print("Level: 1")
            cursor.execute("""select * from freebie.requests a 
                left join freebie.agents b
                on a.agent_name = b.agent
                where a.status = 'Pending'
                and b.team_lead = %(username)s
                and discount_percent <= %(discount)s""", {"username":userId, "discount":5})
        if level == 2:
            print("Level: 2")
            cursor.execute("""select * from freebie.requests a 
                where a.status = 'Pending'
                and a.discount_percent > %(discount_low)s
                and a.discount_percent <= %(discount_high)s""", {"discount_low":5, "discount_high":10})
        if level == 3:
            print("Level: 3")
            cursor.execute("""select * from freebie.requests a 
                where a.status = 'Pending'
                and a.discount_percent > %(discount_low)s
                and a.discount_percent <= %(discount_high)s""", {"discount_low":10, "discount_high":100})
        result = cursor.fetchall()
        cursor.close()
        print(result)
        json_result = methods.convertToJSON(result)
        return json_result

    def updateRequest(requestId, status):
        cursor = tasks.getDBCursor()
        cursor.execute("UPDATE freebie.Requests SET status = %(status)s WHERE id = %(id)s", {"status":status, "id":requestId})
        cursor.close()

    def addRequest(requestData):
        cursor = tasks.getDBCursor()
        query = """INSERT INTO freebie.Requests (agent_name,category,account_phone,sales_date,activation_date,sales_amount,
        prev_sales,discount_amount,discount_percent,alternate_number,discussion_details,status)
        VALUES (%(agent_name)s,%(category)s,%(account_phone)s,%(sales_date)s,%(activation_date)s,%(sales_amount)s,
        %(prev_sales)s,%(discount_amount)s,%(discount_percent)s,%(alternate_number)s,%(discussion_details)s,%(status)s)"""
        cursor.execute(query,requestData)
        cursor.close()
