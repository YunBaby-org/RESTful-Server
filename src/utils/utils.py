from flask import request, make_response, jsonify
import jwt, datetime, psycopg2, os
import src.api.resources.users as User
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
SECRET_KEY = os.getenv('SECRET_KEY')

conn = psycopg2.connect(database=os.getenv('DBDB'), user=os.getenv('DBUSER'), password=os.getenv('DBPASSWORD'), host=os.getenv('DBHOST'), port=os.getenv('DBPORT'))

def getTokenData():
    """
    取得 JWT part2 data
    """
    token = request.cookies.get('JWT_TOKEN')
    return jwt.decode(token, JWT_SECRET_KEY)    # dict

def refreToken():
    """
    update  access token
    """
    reftoken = request.cookies.get('refresh')
    reftokenData = jwt.decode(reftoken, JWT_SECRET_KEY)

    resp = make_response(jsonify({'message': 'New token has been sent'}), 200)
    tokenPayload = {
        'userid': reftokenData['userid'],  
        'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=30)
    }
    newAccessToken = jwt.encode(payload=tokenPayload, key=JWT_SECRET_KEY)
    resp.set_cookie(key='JWT_TOKEN', value=newAccessToken, expires=datetime.datetime.utcnow()+datetime.timedelta(minutes=30))
    return resp


def getTkrData(tkr):
    return {
        'trackerid': tkr[0],
        'name': tkr[1],
        'phone': tkr[2] 
    }
