from flask import request
import jwt, datetime
from .. import JWT_SECRET_KEY
import src.module.User as User

def getTokenData():
    """
    取得 JWT part2 data
    """
    token = request.cookies.get('JWT_TOKEN')
    return jwt.decode(token, JWT_SECRET_KEY)    # dict

def referToken():
    reftoken = request.cookies.get('refresh')
    reftokenData = jwt.decode(reftoken, JWT_SECRET_KEY)
    user = User.User.query.filter_by(id=reftokenData['userid']).first()
    tokenPayload = {
        'userid': user.id, 
        'username': user.username, 
        'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=30)
    }
    return jwt.encode(payload=tokenPayload, key=JWT_SECRET_KEY)
