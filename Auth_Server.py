from flask import Flask, request
from src.auth.auth import login_handler, signup_handler, token_require, logout_handler
import src.utils.utils as utils

app = Flask(__name__)
app.config['SECRET_KEY'] = utils.SECRET_KEY

# 登陸
@app.route('/login', methods=['POST'])
def login():
    if request.method=='POST':
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
    

@app.route('/')
def index():
    return 'Hi'

if __name__=='__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)