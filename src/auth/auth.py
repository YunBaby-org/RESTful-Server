from flask import request, make_response, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import jwt, datetime
from functools import wraps
import src.api.resources.users as User
import src.utils.utils as utils
from .. import JWT_SECRET_KEY
import psycopg2, uuid


def login_handler():
    """
    處裡登陸的事件
    """
    # 抓出 user
    conn = psycopg2.connect(database="testdb", user="postgres", password="123456", host="127.0.0.1", port="5432")
    cur = conn.cursor()
    user_data = "SELECT * FROM users WHERE username = '%s'"%(request.form.get('username'))
    cur.execute(user_data)
    user = cur.fetchone()
    conn.close()
    if user and check_password_hash(user[4], request.form.get('password')):
        # exp time 1hr
        tokenPayload = {
            'userid': user[0], 
            'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=30)
        }
        # 'username': user[1], 
        # 'phone': user[2], 
        refreshPayload = {
            'userid': user[0], 
            'exp':datetime.datetime.utcnow()+datetime.timedelta(weeks=4)
        }
        resp = make_response(jsonify({'message': 'Login Successful'}), 200)
        # 傳送 設定 cookies time
        token = jwt.encode(payload=tokenPayload, key=JWT_SECRET_KEY)
        resp.set_cookie(key='JWT_TOKEN', value=token, expires=datetime.datetime.utcnow()+datetime.timedelta(minutes=30))
        token = jwt.encode(payload=refreshPayload, key=JWT_SECRET_KEY)
        resp.set_cookie(key='refresh', value=token, expires=datetime.datetime.utcnow()+datetime.timedelta(weeks=4))
        return resp
    else:
        return jsonify({'message': 'Username or Password Error!'}), 403

def logout_handler():
    """
    處裡登出的事件
    """
    resp = make_response(jsonify({'message': 'Logout Successful'}), 200)
    # 刪除 cookies
    resp.delete_cookie('JWT_TOKEN')
    resp.delete_cookie('refresh')
    return resp
       
def signup_handler():
    """
    處裡註冊的事件
    """
    try:
        # 把密碼加密
        hashed_pwd = generate_password_hash(request.form.get('password'), method='sha256')
        conn = psycopg2.connect(database="testdb", user="postgres", password="123456", host="127.0.0.1", port="5432")
        #使用 cursor() 方法建立一個遊標物件 cursor
        cur = conn.cursor()
        new_user = "INSERT INTO users (id, username, email, phone, password)\
            VALUES('%s' ,'%s', '%s', '%s', '%s')"%(str(uuid.uuid1()), request.form.get('username'), request.form.get('email'), request.form.get('phone'), hashed_pwd)
        # execute(query, vars=None)：執行 SQL 語句
        cur.execute(new_user)
        # commit()：提交任何未提交的事務到數據庫
        conn.commit()
        # 關閉連接
        conn.close()
        return jsonify({'message': 'Sign up successful'}), 200
    except Exception as e:
        return jsonify({'message': 'Failure'}), 403

def token_require(f):
    """
    token 驗證處理
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('JWT_TOKEN')
        reftoken = request.cookies.get('refresh')
        # 沒有 token
        if not token and not reftoken:
            # 401 or 403
            return jsonify({'message': 'Token is missing, you need login'}), 403
        
        # 判斷 token 是否正確
        try:
            jwt.decode(token, JWT_SECRET_KEY)
        except:
            try:
                jwt.decode(reftoken, JWT_SECRET_KEY)
                resp = make_response(jsonify({'message': 'New token has been sent, please retransmit'}), 200)
                # 拿新的 tkn
                refertoken = utils.referToken()
                print(refertoken)
                resp.set_cookie(key='JWT_TOKEN', value=refertoken, expires=datetime.datetime.utcnow()+datetime.timedelta(minutes=30))
                return resp
            except:
                return jsonify({'message': 'Token is missing or invalid'}), 403
        return f(*args, **kwargs)
    return decorated