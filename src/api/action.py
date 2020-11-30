from flask import request, jsonify
import src.utils.utils as utils
from dotenv import load_dotenv, find_dotenv
import pika, os, uuid,logging,json

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
    tkr_id = request.json.get('tracker_id')

    # 查看是否有這個指令
    if (request_data not in request_dict['Request']):
        return jsonify({'message': 'Request parameters error'}), 400

    try:
        queue_name = "tracker." + tkr_id + ".requests"
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.getenv('RABBITHOST'), port=os.getenv('RABBITPORT')))
        channel = connection.channel()
        
        message = {'Request': request_data, 'id': str(uuid.uuid1())}
        if payload_data !=None:
            message['Payload'] = payload_data
        channel.basic_publish(exchange='', routing_key=queue_name, body=json.dumps(message))
        print(" [O] Sent %r" % message)
        logging.info('send to '+str(queue_name))
        connection.close()
    except Exception as e:
        logging.error(e)
        return jsonify({'message': 'Missing parameters'}), 400

    return jsonify({'message': 'Send Request Successful'}), 200