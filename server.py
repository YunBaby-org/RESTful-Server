from flask import Flask, jsonify, request, make_response
import jwt, datetime, config
from flask_sqlalchemy import SQLAlchemy
from src.module.User import User
from src.module import db
from src.auth.auth import login_handler, signup_handler, token_require, logout_handler
from src.auth import JWT_SECRET_KEY
from src.api.send_request import BrowserToRabbit
from src.api.location import getLocInfo


app = Flask(__name__)
app.config.from_object(config)
# 實例化的數據庫
db.init_app(app)

# 登陸
@app.route('/login', methods=['POST'])
def login():
    if request.method=='POST':
        # return login_handler(request) 
        return login_handler() 

# 登出
@app.route('/logout', methods=['GET'])
@token_require
def logout():
    if request.method=='GET':
        return logout_handler()   

# 註冊
@app.route('/signup', methods=['POST'])
def signup():
    if request.method=='POST':
        return signup_handler()
    
# information
@app.route('/api/v1/resources/users/information', methods=['GET', 'PUT'])
@token_require
def usersInfo():
    # 拿到 user 資訊
    if request.method=='GET':
        data = User.getUserInfo()
        return jsonify({'message': 'UserInfo', 'data': data}), 200
    # 更新 user 資訊
    elif request.method=='PUT':
        # 接收格式為 JSON
        data = User.updateUserInfo(username=request.json.get('username') , email=request.json.get('email'), phone=request.json.get('phone'))
        return jsonify({'message': data})

# location
@app.route('/api/v1/resources/users/location', methods=['GET'])
@token_require
def location():
    if request.method=='GET':
        getLocInfo()
        return 'LOC'

# send-request
@app.route('/api/v1/action/send-request', methods=['POST'])
@token_require
def send_request():
    return BrowserToRabbit()

# boundary
@app.route('/api/v1/resources/users/boundary', methods=['POST'])
@token_require
def boundary():
    pass

# responses
@app.route('/api/v1/resources/users/responses', methods=['GET'])
@token_require
def responses():
    pass





if __name__=='__main__':
    app.run(port=5000, debug=True)