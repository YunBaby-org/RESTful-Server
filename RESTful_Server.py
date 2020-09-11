from flask import Flask, jsonify, request, make_response
import src.api.resources.users as User
from src.auth.auth import token_require
from src.api.action import BrowserToRabbit
import src.utils.utils as utils

app = Flask(__name__)
app.config['SECRET_KEY'] = utils.SECRET_KEY

    
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
        return User.updateUserInfo()

# location
@app.route('/api/v1/resources/users/location', methods=['GET'])
@token_require
def location():
    if request.method=='GET':
        return User.getLocInfo()

# send-request
@app.route('/api/v1/action/send-request', methods=['POST'])
@token_require
def send_request():
    return BrowserToRabbit()

# boundary
@app.route('/api/v1/resources/users/boundary', methods=['GET', 'PUT'])
@token_require
def boundary():
    if request.method=='GET':
        return User.getBoundary()
    elif request.method=='PUT':
        pass

# responses
@app.route('/api/v1/resources/users/responses', methods=['GET'])
@token_require
def responses():
    pass

# trackers
@app.route('/api/v1/resources/users/trackers', methods=['GET'])
@token_require
def trackers():
    return User.getTrackers()


# addtracker
@app.route('/api/v1/resources/users/addtracker', methods=['PUT'])
@token_require
def addtracker():
    return User.addTrackers()

# deltracker
@app.route('/api/v1/resources/users/deltracker', methods=['PUT'])
@token_require
def deltracker():
    return User.delTrackers()

if __name__=='__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)