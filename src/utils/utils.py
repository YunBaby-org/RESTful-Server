from flask import request
import jwt
from .. import JWT_SECRET_KEY

def getTokenData():
    """
    取得 JWT part2 data
    """
    token = request.cookies.get('JWT_TOKEN')
    return jwt.decode(token, JWT_SECRET_KEY)    # dict