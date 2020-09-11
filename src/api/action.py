from flask import request, jsonify
import src.utils.utils as utils
from dotenv import load_dotenv, find_dotenv
import pika, os, uuid

load_dotenv(find_dotenv())

request_dict = {
    'Request': [
        'GetPowerStatus', 'GetDeviceStatus', 'GetVersion', 'ScanGPS', 'ScanWifiSignal', 'ScanTelephoneSignal', 'Ping', 'SetAutoReport', 'SetReportInterval', 'SetPowerSaving'
    ] 
}

def BrowserToRabbit():
    """
    send_request to rabbit
    """
    request_data = request.json.get('Request')
    payload_data = request.json.get('Payload')
    tkrname_data = request.json.get('tracker_name')

    # 查看是否有這個指令
    if (request_data not in request_dict['Request']):
        return jsonify({'message': 'Missing parameters'}), 400

    try:
        cur = utils.conn.cursor()
        tkr_data = "SELECT * FROM trackers WHERE tkrname = '%s'"%(tkrname_data)
        cur.execute(tkr_data)
        tkrname = cur.fetchone()
        queue_name = "tracker." + tkrname[0] + ".requests"
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.getenv('RABBITHOST'), port=os.getenv('RABBITPORT')))
        channel = connection.channel()
        channel.queue_declare(queue=queue_name)
        message = {'Request': request_data, 'id': str(uuid.uuid1())}
        if payload_data !=None:
            message['Payload'] = payload_data
        channel.basic_publish(exchange='', routing_key=queue_name, body=str(message))
        print(" [O] Sent %r" % message)
        connection.close()
    except:
        return jsonify({'message': 'Missing parameters'}), 400

    return jsonify({'message': 'Send Request Successful'}), 200