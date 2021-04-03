
import json

import json
import requests

import logging

from flask import Flask, request, jsonify


application = Flask(__name__)


@application.route('/', methods=['POST'])
def mainmatch():
    if request.method == 'POST':
        data = json.loads(request.data)
        logging.info(data)
        resume_id = data['resume_id']
        usr_text = data['user_text']
        return jsonify({'msg': 'Success HELLO', 'errcode': '200'})


# ************** interface_end **************
if __name__ == "__main__":
    application.run(host="127.0.0.1", port=8092, debug=True)
