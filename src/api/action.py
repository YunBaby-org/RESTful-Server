from flask import request, jsonify

request_dict = {
    'Request': [
        'GetPowerStatus', 'GetDeviceStatus', 'GetVersion', 'ScanGPS', 'ScanWifiSignal', 'ScanTelephoneSignal', 'Ping', 'SetAutoReport', 'SetReportInterval', 'SetPowerSaving'
    ] 
}

# 之後要使用 Pika 套件 -> RabbitMQ
def BrowserToRabbit():
    """
    send_request
    接收 browser 的要求，之後送給 rabbit
    """
    request_data = request.json.get('Request')
    id_data = request.json.get('id')
    # 查看是否有這個指令
    if (request_data not in request_dict['Request']) or id_data==None:
        print('傳送參數錯誤')
        return jsonify({'message': 'Missing parameters'}), 422  

    print('正確無誤')
    return jsonify({'message': 'Send Request Successful'}), 200

