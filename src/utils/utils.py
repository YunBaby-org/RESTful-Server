from flask import request
import jwt, datetime
from .. import JWT_SECRET_KEY
import src.api.resources.users as User
import psycopg2
import os
from dotenv import load_dotenv, find_dotenv

def getTokenData():
    """
    取得 JWT part2 data
    """
    token = request.cookies.get('JWT_TOKEN')
    return jwt.decode(token, JWT_SECRET_KEY)    # dict

def referToken():
    reftoken = request.cookies.get('refresh')
    reftokenData = jwt.decode(reftoken, JWT_SECRET_KEY)

    DB_DATA = getDB()
    conn = psycopg2.connect(database=DB_DATA['DBDB'], user=DB_DATA['DBUSER'], password=DB_DATA['DBPASSWORD'], host=DB_DATA['DBHOST'], port=DB_DATA['DBPORT'])
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

def getDB():
    load_dotenv(find_dotenv())
    DB_DATA = dict()
    DB_DATA['DBDB'] = os.getenv('DBDB')
    DB_DATA['DBUSER'] = os.getenv('DBUSER')
    DB_DATA['DBPASSWORD'] = os.getenv('DBPASSWORD')
    DB_DATA['DBHOST'] = os.getenv('DBHOST')
    DB_DATA['DBPORT'] = os.getenv('DBPORT')
    return DB_DATA