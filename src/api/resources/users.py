import src.utils.utils as utils
from flask import jsonify, Flask, request
import psycopg2, uuid, datetime, pytz
from werkzeug.security import generate_password_hash

def getUserInfo():
    """
    /information [GET]
    獲得個人資料
    """
    tokenData = utils.getTokenData()
    cur = utils.conn.cursor()
    user_data = "SELECT * FROM users WHERE id = '%s'"%(tokenData['userid'])
    cur.execute(user_data)
    user = cur.fetchone()

    return {'userid': user[0], 'username': user[1], 'email': user[2], 'phone': user[3]}

def updateUserInfo():
    """
    /information [PUT]
    修改個人資料
    """
    tokenData = utils.getTokenData()

    try:
        cur = utils.conn.cursor()
        hashed_pwd = generate_password_hash(request.form.get('password'), method='sha256')
        update_data = "UPDATE users set email='%s', phone='%s', password='%s' where id='%s'"%(request.form.get('email'), request.form.get('phone'), hashed_pwd, tokenData['userid'])
        cur.execute(update_data)
        utils.conn.commit()
        return jsonify({'message': 'Update finished'}), 200
    except Exception as e:
        print(e)
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

def addBoundary():
    """
    /boundary [POST]
    """
    try:
        bnd_data = request.json.get('boundary')
        tkr_id = request.json.get('tkr_id')
        cur = utils.conn.cursor()
        add_bnd = "INSERT INTO boundary (id, tracker_id, time_start, time_end, lat, lng, radius)\
            VALUES('%s','%s', '%s', '%s', %f, %f, %d)"%(str(uuid.uuid1()), tkr_id, bnd_data['time_start'], bnd_data['time_end'], bnd_data['lat'], bnd_data['lng'], bnd_data['radius'])
        cur.execute(add_bnd)
        utils.conn.commit()
        return jsonify({'message': 'Successful'}), 201
    except:
        return jsonify({'message': 'Failure'}), 400
        

def getBoundary():
    """
    /boundary [GET]
    """
    bnd_mode = int(request.args.get('mode'))
    tkr_id = request.args.get('tracker')
    tw = pytz.timezone('Asia/Taipei') # 建立一個時區物件
    current_time = datetime.datetime.now(tw).strftime("%Y-%m-%d %H:%M:%S%z")
    cur = utils.conn.cursor()
    print(type(current_time))
    result = list()
    if bnd_mode==0:
        bnd_data = "SELECT * FROM boundary WHERE tracker_id = '%s'"%(tkr_id)
        cur.execute(bnd_data)
        bnds = cur.fetchall()
        if bnds:
            for bnd in bnds:
                result.append(utils.getBndData(bnd))
            return jsonify({"boundarys": result}), 200
        else:
            return jsonify({"message": "No boundary"}), 200
    elif bnd_mode==1:
        bnd_data = "SELECT * FROM boundary WHERE tracker_id = '%s' and timestamptz'%s'>=time_start and timestamptz'%s'<=time_end"\
            %(tkr_id, current_time, current_time)
        cur.execute(bnd_data)
        bnds = cur.fetchall()
        print(bnds)
        if bnds:
            for bnd in bnds:
                result.append(utils.getBndData(bnd))
            return jsonify({"boundarys": result}), 200
        else:
            return jsonify({"message": "No boundary"}), 200
    else:
        return jsonify({"message": "Mode error"}), 400

def updateBoundary():
    """
    /boundary [PUT]
    """
    bnd_data = request.json.get('boundary')
    bnd_id = request.json.get('bnd_id')
    cur = utils.conn.cursor()
    update_data = "UPDATE boundary set time_start='%s', time_end='%s', lat=%f, lng=%f, radius=%d where id='%s'"%(bnd_data['time_start'], bnd_data['time_end'], bnd_data['lat'], bnd_data['lng'], bnd_data['radius'], bnd_id)
    cur.execute(update_data)
    utils.conn.commit()
    return jsonify({'message': 'Successful'}), 201

def delBoundary():
    """
    /delBoundary [DELETE]
    """
    try:
        cur = utils.conn.cursor()
        del_tkr = "DELETE FROM boundary WHERE id='%s'"%(request.json.get('id'))
        cur.execute(del_tkr)
        utils.conn.commit()
        return jsonify({'message': 'Del successful'}), 200
    except:
        return jsonify({'message': 'Failure'}), 400

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
    
    cur = utils.conn.cursor()
    tkr_data = "SELECT * FROM trackers WHERE user_id = '%s'"%(tokenData['userid'])
    cur.execute(tkr_data)
    tkrs = cur.fetchall()
    tkr_datas = dict()
    if tkrs:
        for tkr in tkrs:
            tkr_datas[tkr[0]] = (utils.getTkrData(tkr))
        return jsonify({"trackers": tkr_datas}), 200
    else:
        return jsonify({"message": "No boundary"}), 200

def addTrackers():
    """
    /addtracker [POST]
    """
    tokenData = utils.getTokenData()
    try:
        cur = utils.conn.cursor()
        tkr_id = str(uuid.uuid1())
        new_tkr = "INSERT INTO trackers (id, tkrname, phone, user_id)\
            VALUES('%s' ,'%s', '%s', '%s')"%(tkr_id, request.form.get('name'), request.form.get('phone'), tokenData['userid'])
        cur.execute(new_tkr)
        utils.conn.commit()
        return jsonify({'tracker_id': tkr_id}), 201
    except:
        return jsonify({'message': 'Failure'}), 400

def delTrackers():
    """
    /deltracker [DELETE]
    """
    try:
        cur = utils.conn.cursor()
        del_tkr = "DELETE FROM trackers WHERE id='%s'"%(request.json.get('id'))
        cur.execute(del_tkr)
        utils.conn.commit()
        return jsonify({'message': 'Del successful'}), 200
    except:
        return jsonify({'message': 'Failure'}), 400