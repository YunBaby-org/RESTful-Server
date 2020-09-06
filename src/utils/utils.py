from flask import request
import jwt, datetime
from .. import JWT_SECRET_KEY
import src.api.resources.users as User
import psycopg2

def getTokenData():
    """
    取得 JWT part2 data
    """
    token = request.cookies.get('JWT_TOKEN')
    return jwt.decode(token, JWT_SECRET_KEY)    # dict

def referToken():
    reftoken = request.cookies.get('refresh')
    reftokenData = jwt.decode(reftoken, JWT_SECRET_KEY)

    conn = psycopg2.connect(database="testdb", user="postgres", password="123456", host="127.0.0.1", port="5432")
    cur = conn.cursor()
    user_data = "SELECT * FROM users WHERE id = '%s'"%(reftokenData['userid'])
    cur.execute(user_data)
    user = cur.fetchone()
    conn.close()

    tokenPayload = {
        'userid': user[0],  
        'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=30)
    }
    return jwt.encode(payload=tokenPayload, key=JWT_SECRET_KEY)


def getTkrData(tkr):
    return {
        'trackerid': tkr[0],
        'name': tkr[1],
        'phone': tkr[2] 
    }