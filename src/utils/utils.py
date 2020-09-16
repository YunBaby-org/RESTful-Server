from flask import request, make_response, jsonify
import jwt, psycopg2, os
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
    return jwt.decode(token, JWT_SECRET_KEY)

def getTkrData(tkr):
    return {
        'trackerid': tkr[0],
        'name': tkr[1],
        'phone': tkr[2] 
    }

def getBndData(bnd):
    return {
        'id': bnd[0],
        'time_start': str(bnd[2]),
        'time_end': str(bnd[3]),
        'lat': bnd[4],
        'lng': bnd[5],
        'radius': bnd[6]
    }