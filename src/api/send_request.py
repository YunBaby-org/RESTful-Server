from flask import request, jsonify

request_dict = {
    'Request': [
        'GetPowerStatus', 'GetDeviceStatus', 'GetVersion', 'ScanGPS', 'ScanWifiSignal', 'ScanTelephoneSignal', 'Ping', 'SetAutoReport', 'SetReportInterval', 'SetPowerSaving'
    ] 
}

# 之後要使用 Pika 套件 -> RabbitMQ
def BrowserToRabbit():
    """
    接收 browser 的要求，之後送給 rabbit
    """
    request_data = request.json.get('Request')
    # 查看是否有這個指令
    if request_data not in request_dict['Request']:
        print('找不到')
        return jsonify({'message': 'Missing parameters'}), 422

        pass

    print('找到囉')
    return jsonify({'message': 'Send Request Successful'}), 200

