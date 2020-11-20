import json
from flask import Flask,request
from flask_cors import CORS
from SearchAndRecommend.dao import config
from RecommandModule.service import Resume2Job
from RecommandModule.service import Job2Resume
import os

_project_root = os.path.dirname(os.path.realpath(__file__))


app=Flask(__name__)
CORS(app)


#如果以后有模型，切换到模型地址加载
resumeModel = Resume2Job
jobModel = Job2Resume

@app.route('/rec/res',methods=['POST'])
def res_service():
    data = json.loads(request.data.decode("utf-8"))
    result = resumeModel.getRecommandJob(data)

    return app.make_response((result,200,{"Content-Type":"application/josn;charset=utf-8"}))

@app.route('/rec/job',methods=['POST'])
def job_service():
    data = json.load(request.data.decode("utf-8"))
    result = jobModel.getRecommadResume(data)
    return app.make_response((result,200,{"Content-Type":"application/josn;charset=utf-8"}))

@app.route('/rec/request_test',methods=['GET'])
def res_request_test():
    return app.make_response(("connect success!",200,{"Content-Type":"application/josn;charset=utf-8"}))

if __name__ == "__main__":
    app.debug=True
    host = config.configer.get("server", "host")
    port = config.configer.get("server", "port")
    app.run(host=host,port=port,debug=False,threaded=True)



