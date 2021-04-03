import sys
sys.path.append('/home/iotlab/Search/')
from service.ResumeInfoService import RIS
import json
import logging

from flask import Flask, request

application = Flask(__name__)
application.config['JSON_AS_ASCII'] = False
logging.basicConfig(filename='rs.log',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO)

@application.route('/resume_present', methods=['POST'])
def present_process():
    if request.method == 'POST':
        data = json.loads(request.data.decode("utf-8"))
        logging.info("the input request data is as follow")
        logging.info(data)
        result = RIS.present_process(data)
        # data = json.dumps(data, ensure_ascii=False)
        logging.info("the result is {}".format(str(result)))
        return application.make_response((result, 200, {"Content-Type": "application/json;charset=utf-8"}))


# ************** interface_end **************
if __name__ == "__main__":
    application.run(host="0.0.0.0", port=8093, debug=False)
