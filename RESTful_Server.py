from flask import Flask, jsonify, request
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
    if request.method=='GET':
        data = User.getUserInfo()
        return jsonify({'message': 'UserInfo', 'data': data}), 200
    elif request.method=='PUT':
        return User.updateUserInfo()

# location
@app.route('/api/v1/resources/users/location', methods=['GET'])
@token_require
def location():
    return User.getLocInfo()

# send-request
@app.route('/api/v1/action/send-request', methods=['POST'])
@token_require
def send_request():
    return BrowserToRabbit()

# boundary
@app.route('/api/v1/resources/users/boundary', methods=['GET', 'PUT', 'POST', 'DELETE'])
@token_require
def boundary():
    if request.method=='GET':
        return User.getBoundary()
    elif request.method=='POST':
        return User.addBoundary()
    elif request.method=='PUT':
        return User.updateBoundary()
    elif request.method=='DELETE':
        return User.delBoundary()

# responses
@app.route('/api/v1/resources/users/responses', methods=['GET'])
@token_require
def responses():
    pass

# trackers
@app.route('/api/v1/resources/users/trackers', methods=['GET', 'POST', 'DELETE' ])
@token_require
def trackers():
    if request.method=='GET':
        return User.getTrackers()
    elif request.method=='POST':
        return User.addTrackers()
    elif request.method=='DELETE':
        return User.delTrackers()

if __name__=='__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)