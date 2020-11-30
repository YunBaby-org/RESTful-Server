from flask import Flask, jsonify, request
import src.api.resources.users as User
from src.auth.auth import token_require
from src.api.action import BrowserToRabbit
import src.utils.utils as utils
import logging
app = Flask(__name__)
app.config['SECRET_KEY'] = utils.SECRET_KEY

    
# information
@app.route('/api/v1/resources/users/information', methods=['GET', 'PUT'])
@token_require
def usersInfo():
    logging.info('/api/v1/resources/users/information '+str(request.method))
    if request.method=='GET':
        data = User.getUserInfo()
        return jsonify({'message': 'UserInfo', 'data': data}), 200
    elif request.method=='PUT':
        return User.updateUserInfo()

# location
@app.route('/api/v1/resources/users/location', methods=['GET'])
@token_require
def location():
    logging.info('/api/v1/resources/users/location '+str(request.method))
    return User.getLocInfo()

# send-request
@app.route('/api/v1/action/send-request', methods=['POST'])
@token_require
def send_request():
    logging.info('/api/v1/action/send-request '+str(request.method))
    return BrowserToRabbit()

# boundary
@app.route('/api/v1/resources/users/boundary', methods=['GET', 'PUT', 'POST', 'DELETE'])
@token_require
def boundary():
    logging.info('/api/v1/resources/users/boundary '+str(request.method))
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
    logging.info('/api/v1/resources/users/trackers '+str(request.method))
    if request.method=='GET':
        return User.getTrackers()
    elif request.method=='POST':
        return User.addTrackers()
    elif request.method=='DELETE':
        return User.delTrackers()

if __name__=='__main__':
    logging.getLogger().setLevel(logging.INFO)
    logging.info("Restful Server Start at port 5001")
    app.run(host='0.0.0.0', port=5001)