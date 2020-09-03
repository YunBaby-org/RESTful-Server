from . import db
import src.utils.utils as utils
from flask import jsonify, Flask, request


print('--- User & Tarcker ---')
class User(db.Model):
    """
    User model
    """
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    phone = db.Column(db.String(10), unique=True)
    password = db.Column(db.String(80))
    tkrs = db.relationship("Trackers", backref="user")
    
    def getUserInfo():
        """
        /information [GET]
        獲得個人資料
        """
        tokenData = utils.getTokenData()
        user = User.query.filter_by(id=tokenData['userid']).first()
        return {'userId': user.id, 'username': user.username, 'email': user.email, 'phone': user.phone}

    # def updateUserInfo(username=None, email=None, phone=None):
    def updateUserInfo():
        """
        /information [PUT]
        修改個人資料
        """
        tokenData = utils.getTokenData()
        try:
            user = User.query.filter_by(id=tokenData['userid']).first()

            username = request.form.get('username')
            email = request.form.get('email')
            phone = request.form.get('phone')

            if username!=None:
                user.username = username
            if email!=None:
                user.email = email
            if phone!=None:
                user.phone = phone
            db.session.commit()

            return {'message': 'Update finished'}
        except Exception as e:
            return jsonify({'message': 'Failure'}), 403 

    def getLocInfo():
        """
        /location [GET]
        不需要傳任何參數
        """
        tokenData = utils.getTokenData()
        print(tokenData['userid'])
        _userLoc = '問 DB'
        _from = '問 DB'
        _to = '問 DB'
        _max = '問 DB'
        _offset = '問 DB'
        _timezone = '問 DB'
        _amount = '問 DB'
        return jsonify({
            'message': {
                'userLocation': _userLoc,
                'amount': _amount,
                'max': _max,
                'from': _from,
                'to': _to,
                'offset': _offset,
                'timezone': _timezone
            }
        }), 200

    def getBoundary():
        """
        /boundary [PUT]
        """
        pass

    def getResponses():
        """
        /responses [GET]
        """
        pass

    def getTrackers():
        """
        /trackers [GET]
        """
        tokenData = utils.getTokenData()
        user = User.query.filter_by(id=tokenData['userid']).first()
        print(user.tkrs)
        tkr_datas = dict()
        for tkr in user.tkrs:
            print('----- info -----')
            tkr_datas[tkr.id] = (utils.getTkrData(tkr))
        return jsonify({
            "trackers": tkr_datas
        }), 200

    def addTrackers():
        """
        /addtracker [POST]
        """
        tokenData = utils.getTokenData()
        try:
            new_tkr = Trackers(tkrname=request.form.get('name'), phone=request.form.get('phone'), user_id=tokenData['userid'])
            db.session.add(new_tkr)
            db.session.commit()
            return jsonify({'message': 'Add successful'}), 200
        except Exception as e:
            return jsonify({'message': 'Failure'}), 403 

    def delTrackers():
        """
        /deltracker [PUT]
        """
        try:
            print(request.json.get('id'))
            print(type(request.json.get('id')))
            tkr = Trackers.query.filter(Trackers.id==request.json.get('id')).delete()
            db.session.commit()
            return jsonify({'message': 'Del successful'}), 200
        except Exception as e:
            return jsonify({'message': 'Failure'}), 403 


class Trackers(db.Model):
    __tablename__ = 'trackers'
    id = db.Column(db.Integer, primary_key=True)
    tkrname = db.Column(db.String(15), unique=True)
    # tkrname = db.Column(db.String(15))
    phone = db.Column(db.String(10), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    