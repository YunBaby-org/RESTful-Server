from flask import Flask, request
import config
from flask_sqlalchemy import SQLAlchemy
from src.module import db
from src.auth.auth import login_handler, signup_handler, token_require, logout_handler

app = Flask(__name__)
app.config.from_object(config)
# 實例化的數據庫
db.init_app(app)

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
    

if __name__=='__main__':
    app.run(port=5000, debug=True)