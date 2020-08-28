from flask import Flask, jsonify, request, make_response
import config
from flask_sqlalchemy import SQLAlchemy
from src.module.User import User
from src.module import db
from src.auth.auth import token_require
from src.auth import JWT_SECRET_KEY
from src.api.send_request import BrowserToRabbit
from src.api.location import getLocInfo


app = Flask(__name__)
app.config.from_object(config)
# 實例化的數據庫
db.init_app(app)

    
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
    app.run(port=5001, debug=True)