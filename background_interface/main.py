import sys
sys.path.append('/home/iotlab/Search/')
from background_interface.service.keyInfoService import KS
import json
import logging

from flask import Flask, request, jsonify
application = Flask(__name__)
application.config['JSON_AS_ASCII'] = False


@application.route('/query_data_by_page', methods=['POST'])
def query_data_by_page():
    if request.method == 'POST':
        data = json.loads(request.data)
        logging.info("the input request data is as follow")
        logging.info(data)
        key_name = data['key_name']
        curr_page = data['curr_page']
        page_size = data['page_size']
        return jsonify(KS.query_data_by_page(key_name, curr_page, page_size))

@application.route('/update_isStop', methods=['POST'])
def update_isStop():
    if request.method == 'POST':
        data = json.loads(request.data)
        logging.info("the input request data is as follow")
        logging.info(data)
        recordId = data['recordId']
        isStop = data['isStop']
        KS.update_isStop(recordId, isStop)
        return jsonify({'state':"success"})

@application.route('/add_analyze_token', methods=['POST'])
def add_analyze_token():
    if request.method == 'POST':
        data = json.loads(request.data)
        logging.info("the input request data is as follow")
        logging.info(data)
        recordId = data['recordId']
        token = data['token']
        KS.add_analyze_token(recordId, token)
        return jsonify({'state':"success"})

@application.route('/remove_analyze_token', methods=['POST'])
def remove_analyze_token():
    if request.method == 'POST':
        data = json.loads(request.data)
        logging.info("the input request data is as follow")
        logging.info(data)
        recordId = data['recordId']
        token = data['token']
        KS.remove_analyze_token(recordId, token)
        return jsonify({'state':"success"})

# ************** interface_end **************
if __name__ == "__main__":
    application.run(host="0.0.0.0", port=8092, debug=True)
