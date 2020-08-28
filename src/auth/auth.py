from . import db, User, JWT_SECRET_KEY
from flask import request, make_response, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import jwt, datetime
from functools import wraps

def login_handler():
    """
    處裡登陸的事件
    """
    # 抓出 user
    user = User.query.filter_by(username=request.form.get('username')).first()
    if user and check_password_hash(user.password, request.form.get('password')):
        # exp time 1hr
        tokenPayload = {
            'userid': user.id, 
            'username': user.username, 
            'exp':datetime.datetime.utcnow()+datetime.timedelta(hours=1)
        }
        token = jwt.encode(payload=tokenPayload, key=JWT_SECRET_KEY)
        resp = make_response(jsonify({'message': 'Login Successful'}), 200)
        # 傳送 設定 cookies time
        resp.set_cookie(key='JWT_TOKEN', value=token, expires=datetime.datetime.utcnow()+datetime.timedelta(hours=1))
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
    return resp
       
def signup_handler():
    """
    處裡註冊的事件
    """
    try:
        # 把密碼加密
        hashed_pwd = generate_password_hash(request.form.get('password'), method='sha256')
        new_user = User(username=request.form.get('username'), email=request.form.get('email'), phone=request.form.get('phone'), password=hashed_pwd)
        # 丟 db 裡面
        db.session.add(new_user)
        db.session.commit()
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
        # 沒有 token
        if not token:
            # 401 or 403
            return jsonify({'message': 'Token is missing, you need login'}), 403
        
        # 判斷 token 是否正確
        try:
            data = jwt.decode(token, JWT_SECRET_KEY)
        except:
            return jsonify({'message': 'Token is missing or invalid'}), 403

        return f(*args, **kwargs)
    return decorated