from flask import request, jsonify
from . import utils


def getLocInfo():
    """
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
    })