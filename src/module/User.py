from . import db
from ..utils import utils

class User(db.Model):
    """
    User model
    """
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    phone = db.Column(db.String(10), unique=True)
    password = db.Column(db.String(80))
    
    
    def getUserInfo():
        """
        獲得個人資料
        """
        tokenData = utils.getTokenData()
        user = User.query.filter_by(id=tokenData['userid']).first()
        return {'userId': user.id, 'username': user.username, 'email': user.email, 'phone': user.phone}

    
    def updateUserInfo(username=None, email=None, phone=None):
        """
        修改個人資料
        """
        tokenData = utils.getTokenData()
        user = User.query.filter_by(id=tokenData['userid']).first()
        if username!=None:
            user.username = username
        if email!=None:
            user.email = email
        if phone!=None:
            user.phone = phone
        db.session.commit()
        return {'message': 'Update finished'}