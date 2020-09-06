import src.utils.utils as utils
from flask import jsonify, Flask, request
import psycopg2, uuid
from werkzeug.security import generate_password_hash

def getUserInfo():
    """
    /information [GET]
    獲得個人資料
    """
    tokenData = utils.getTokenData()
    conn = psycopg2.connect(database="testdb", user="postgres", password="123456", host="127.0.0.1", port="5432")
    cur = conn.cursor()
    user_data = "SELECT * FROM users WHERE id = '%s'"%(tokenData['userid'])
    cur.execute(user_data)
    user = cur.fetchone()
    conn.close()
    return {'userid': user[0], 'username': user[1], 'email': user[2], 'phone': user[3]}

def updateUserInfo():
    """
    /information [PUT]
    修改個人資料
    """
    tokenData = utils.getTokenData()

    try:
        conn = psycopg2.connect(database="testdb", user="postgres", password="123456", host="127.0.0.1", port="5432")
        cur = conn.cursor()
        hashed_pwd = generate_password_hash(request.form.get('password'), method='sha256')
        update_data = "UPDATE users set email='%s', phone='%s', password='%s' where id='%s'"%(request.form.get('email'), request.form.get('phone'), hashed_pwd, tokenData['userid'])
        cur.execute(update_data)
        conn.commit()
        conn.close()
        return jsonify({'message': 'Update finished'}), 200
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

def putBoundary():
    """
    /boundary [PUT]
    """
    pass

def getBoundary():
    """
    /boundary [GET]
    """
    tracker_id = request.args.get('tracker')
    boundary = {"boundary":{
        "lat":123,
        "lng":456,
        "radius":30
    }}
    return jsonify(boundary), 200

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
    conn = psycopg2.connect(database="testdb", user="postgres", password="123456", host="127.0.0.1", port="5432")
    cur = conn.cursor()
    tkr_data = "SELECT * FROM trackers WHERE user_id = '%s'"%(tokenData['userid'])
    cur.execute(tkr_data)
    tkrs = cur.fetchall()
    tkr_datas = dict()
    for tkr in tkrs:
        print('----- info -----')
        tkr_datas[tkr[0]] = (utils.getTkrData(tkr))
    return jsonify({
        "trackers": tkr_datas
    }), 200

def addTrackers():
    """
    /addtracker [POST]
    """
    tokenData = utils.getTokenData()
    try:
        conn = psycopg2.connect(database="testdb", user="postgres", password="123456", host="127.0.0.1", port="5432")
        cur = conn.cursor()
        new_tkr = "INSERT INTO trackers (id, tkrname, phone, user_id)\
            VALUES('%s' ,'%s', '%s', '%s')"%(str(uuid.uuid1()), request.form.get('name'), request.form.get('phone'), tokenData['userid'])
        cur.execute(new_tkr)
        conn.commit()
        conn.close()
        return jsonify({'message': 'Add successful'}), 200
    except Exception as e:
        return jsonify({'message': 'Failure'}), 403 

def delTrackers():
    """
    /deltracker [PUT]
    """
    try:
        conn = psycopg2.connect(database="testdb", user="postgres", password="123456", host="127.0.0.1", port="5432")
        cur = conn.cursor()
        del_tkr = "DELETE FROM trackers WHERE id='%s'"%(request.json.get('id'))
        cur.execute(del_tkr)
        conn.commit()
        conn.close()
        return jsonify({'message': 'Del successful'}), 200
    except Exception as e:
        return jsonify({'message': 'Failure'}), 403 
   