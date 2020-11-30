from flask import Flask, request, jsonify
from src.auth.auth import login_handler, signup_handler, token_require, logout_handler, refreToken
import src.utils.utils as utils
import logging
app = Flask(__name__)
app.config['SECRET_KEY'] = utils.SECRET_KEY

# 登陸
@app.route('/login', methods=['POST'])
def login():
    logging.info('/api/v1/auth/login '+str(request.method))
    return login_handler() 

# 登出
@app.route('/logout', methods=['GET'])
@token_require
def logout():
    logging.info('/api/v1/auth/logout '+str(request.method))
    return logout_handler()   

# 註冊
@app.route('/signup', methods=['POST'])
def signup():
    logging.info('/api/v1/auth/signup '+str(request.method))
    return signup_handler()
    
@app.route('/refreshToken', methods=['POST'])
def refreshToken():
    logging.info('/api/v1/auth/refreshToken '+str(request.method))
    return refreToken()

@app.route('/me')
@token_require
def me():
    logging.info('/api/v1/auth/me '+str(request.method))
    return jsonify({'status': 'ok'})

@app.route('/')
def index():
    return 'Hi'

if __name__=='__main__':
    logging.getLogger().setLevel(logging.INFO)
    logging.info("Auth_Server Start at port 5000")
    app.run(host='0.0.0.0', port=5000)