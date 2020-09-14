from flask import Flask, request, jsonify
from src.auth.auth import login_handler, signup_handler, token_require, logout_handler, refreToken
import src.utils.utils as utils

app = Flask(__name__)
app.config['SECRET_KEY'] = utils.SECRET_KEY

# 登陸
@app.route('/login', methods=['POST'])
def login():
    return login_handler() 

# 登出
@app.route('/logout', methods=['GET'])
@token_require
def logout():
    return logout_handler()   

# 註冊
@app.route('/signup', methods=['POST'])
def signup():
    return signup_handler()
    
@app.route('/refreshToken', methods=['POST'])
def refreshToken():
    return refreToken()

@app.route('/me')
@token_require
def me():
    return jsonify({'status': 'ok'})

@app.route('/')
def index():
    return 'Hi'

if __name__=='__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)