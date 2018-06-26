from project.api.tasks import tasks
from datetime import datetime

class methods:
    def authenticate(user, password):
        cursor = tasks.getDBCursor()
        cursor.execute("SELECT * FROM pms.Freebie_Users WHERE username = %(username)s OR email = %(username)s", {"username":user})
        result = cursor.fetchone()
        cursor.close()
        if result:
            if result[1] == password:
                return True
        return False

    def verify(user, token):
        cursor = tasks.getDBCursor()
        cursor.execute("SELECT * FROM pms.Freebie_Sessions where username = %(username)s", {"username":user})
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
                "created_at":result[0],
                "id":result[1],
                "agent_name":result[2],
                "category":result[3],
                "user_id":result[4],
                "account_phone":result[5],
                "sales_date":result[6],
                "activation_date":result[7],
                "sales_amount":result[8],
                "prev_sales":result[9],
                "discount_amount":result[10],
                "discount_percent":float(result[11]),
                "alternate_number":result[12],
                "discussion_details":result[13],
                "status":result[14],
                "comment":result[15],
                "updated_by":result[16]
            }
            outJSON.append(row)
        return outJSON

    def getRequests(userId):
        cursor = tasks.getDBCursor()
        cursor.execute("SELECT userlevel FROM pms.Freebie_Users where username = %(username)s", {"username":userId})
        user = cursor.fetchone()
        level = user[0]
        if level == 0:
            cursor.execute("""select * from pms.Freebie_Requests a
                left join pms.Freebie_Agents b
                on a.agent_name = b.agent
                where b.team_lead = %(username)s""", {"username":userId})
        if level == 1:
            cursor.execute("""select * from pms.Freebie_Requests a 
                left join pms.Freebie_Agents b
                on a.agent_name = b.agent
                where b.team_lead = %(username)s""", {"username":userId})
        if level == 2:
            cursor.execute("""select * from pms.Freebie_Requests a 
                left join pms.Freebie_Agents b
                on a.agent_name = b.agent
                where b.manager = %(username)s""", {"username":userId})
        if level == 3:
            cursor.execute("select * from pms.Freebie_Requests a")
        result = cursor.fetchall()
        cursor.close()
        json_result = methods.convertToJSON(result)
        json_result = methods.getActions(level, json_result)
        return json_result

    def updateRequest(requestId, status, comment, user):
        cursor = tasks.getDBCursor()
        cursor.execute("UPDATE pms.Freebie_Requests SET status = %(status)s, comment = %(comment)s, updated_by = %(updated_by)s WHERE id = %(id)s", {"status":status, "comment":comment, "updated_by":user, "id":requestId})
        cursor.close()

    def addRequest(requestData):
        cursor = tasks.getDBCursor()
        timestamp = str(datetime.now())
        requestParam = {}
        for key in requestData:
            requestParam[key] = requestData[key]
        requestParam["created_at"] = str(datetime.now())
        if float(requestData["discount_percent"]) <= 10:
            query = """INSERT INTO pms.Freebie_Requests (created_at,agent_name,category,user_id,account_phone,sales_date,activation_date,
            sales_amount,prev_sales,discount_amount,discount_percent,alternate_number,discussion_details,status, updated_by)
            VALUES (%(created_at)s,%(agent_name)s,%(category)s,%(user_id)s,%(account_phone)s,%(sales_date)s,%(activation_date)s,
            %(sales_amount)s,%(prev_sales)s,%(discount_amount)s,%(discount_percent)s,%(alternate_number)s,
            %(discussion_details)s,'Approved','AutoApproval')"""
        else:
            query = """INSERT INTO pms.Freebie_Requests (created_at,agent_name,category,user_id,account_phone,sales_date,activation_date,
            sales_amount,prev_sales,discount_amount,discount_percent,alternate_number,discussion_details,status)
            VALUES (%(created_at)s,%(agent_name)s,%(category)s,%(user_id)s,%(account_phone)s,%(sales_date)s,%(activation_date)s,
            %(sales_amount)s,%(prev_sales)s,%(discount_amount)s,%(discount_percent)s,%(alternate_number)s,%(discussion_details)s,
            %(status)s)"""
        cursor.execute(query,requestParam)
        cursor.close()

    def getAgents():
        cursor = tasks.getDBCursor()
        cursor.execute("SELECT agent FROM pms.Freebie_Agents")
        agents = cursor.fetchall()
        cursor.close()
        agent_list = [i[0] for i in agents]
        return agent_list;
    
    def getActions(userlevel, results):
        for result in results:
            if result['status'] != 'Pending' or userlevel == 0:
                result['action'] = False
            elif userlevel == 1 and float(result['discount_percent']) < 16:
                result['action'] = True
            elif userlevel == 2 and float(result['discount_percent']) < 26:
                result['action'] = True
            elif userlevel == 3:
                result['action'] = True
            else:
                result['action'] = False
        return results
