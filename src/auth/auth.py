from flask import request, make_response, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import jwt, datetime, psycopg2, uuid
from functools import wraps
import src.api.resources.users as User
import src.utils.utils as utils

def login_handler():
    """
    login handler
    """
    # 抓出 user
    cur = utils.conn.cursor()
    user_data = "SELECT * FROM users WHERE email = '%s'"%(request.form.get('email'))
    cur.execute(user_data)
    user = cur.fetchone()

    if user and check_password_hash(user[4], request.form.get('password')):
        # exp time 30m
        tokenPayload = {
            'userid': user[0], 
            'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=30)
        }
        refreshPayload = {
            'userid': user[0], 
            'exp':datetime.datetime.utcnow()+datetime.timedelta(weeks=4)
        }
        resp = make_response(jsonify({'message': 'Login Successful'}), 200)
        # 傳送 設定 cookies time
        token = jwt.encode(payload=tokenPayload, key=utils.JWT_SECRET_KEY)
        resp.set_cookie(key='JWT_TOKEN', value=token, expires=datetime.datetime.utcnow()+datetime.timedelta(minutes=30))
        token = jwt.encode(payload=refreshPayload, key=utils.JWT_SECRET_KEY)
        resp.set_cookie(key='refresh', value=token, expires=datetime.datetime.utcnow()+datetime.timedelta(weeks=4))
        return resp
    else:
        return jsonify({'message': 'Email or Password Error!'}), 403

def logout_handler():
    """
    logout handler
    """
    resp = make_response(jsonify({'message': 'Logout Successful'}), 200)
    # 刪除 cookies
    resp.delete_cookie('JWT_TOKEN')
    resp.delete_cookie('refresh')
    return resp
       
def signup_handler():
    """
    signup handler
    """
    try:
        # 把密碼加密
        hashed_pwd = generate_password_hash(request.form.get('password'), method='sha256')
        
        #使用 cursor() 方法建立一個遊標物件 cursor
        cur = utils.conn.cursor()
        new_user = "INSERT INTO users (id, username, email, phone, password)\
            VALUES('%s' ,'%s', '%s', '%s', '%s')"%(str(uuid.uuid1()), request.form.get('username'), request.form.get('email'), request.form.get('phone'), hashed_pwd)
        # execute(query, vars=None)：執行 SQL 語句
        cur.execute(new_user)
        # commit()：提交任何未提交的事務到數據庫
        utils.conn.commit()

        return jsonify({'message': 'Sign up successful'}), 200
    except:
        return jsonify({'message': 'Failure'}), 403

def refreToken():
    """
    update access token
    """
    reftoken = request.cookies.get('refresh')
    reftokenData = jwt.decode(reftoken, utils.JWT_SECRET_KEY)

    resp = make_response(jsonify({'message': 'New token has been sent'}), 200)
    tokenPayload = {
        'userid': reftokenData['userid'],  
        'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=30)
    }
    newAccessToken = jwt.encode(payload=tokenPayload, key=utils.JWT_SECRET_KEY)
    resp.set_cookie(key='JWT_TOKEN', value=newAccessToken, expires=datetime.datetime.utcnow()+datetime.timedelta(minutes=30))
    return resp

def token_require(f):
    """
    token 驗證處理
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('JWT_TOKEN')
        # 沒有 token
        if not token:
            return jsonify({'message': 'Token is missing , you need login or refre'}), 401
        
        # 判斷 token 是否正確
        try:
            jwt.decode(token, utils.JWT_SECRET_KEY)
        except:
            return jsonify({'message': 'Token is missing or invalid'}), 401
        return f(*args, **kwargs)
    return decorated