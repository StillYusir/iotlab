from flask_cors import CORS
import os
from flask import Flask,Response,request
import json
from SearchAndRecommend.dao import config
from elasticsearch import  Elasticsearch
from SearchModule.service.search import ESearch
es=Elasticsearch([{'host': '127.0.0.1', 'port': 9200}])

model=ESearch()

_project_root = os.path.dirname(os.path.realpath(__file__))

app=Flask(__name__)
CORS(app)

@app.route('/api/pos-result',methods=['POST'])
def pos_service():
    data=json.loads(request.data.decode("utf-8"))
    #redis 搜索
    # result=GetInfo(data)
    # print(result)#
    # if result !=None:
    #     return app.make_response((result,200,{"Content-Type":"application/josn;charset=utf-8"}))
    # else:
        # print('无缓存')
    try:
        result=model.S_Job(data)
        print("search_result:",result)
        # Redis_save(data,result)
        return app.make_response((result,200,{"Content-Type":"application/josn;charset=utf-8"}))
    except:
        return app.make_response(({"查询失败":"查询失败"},500,{"Content-Type":"application/josn;charset=utf-8"}))

@app.route('/api/resume_result',methods=['POST'])
def res_service():
    data = json.loads(request.data.decode("utf-8"))
    # result=GetInfo(data)
    # if result !=None:
    #     return app.make_response((result,200,{"Content-Type":"application/josn;charset=utf-8"}))
    # else:
    try:
        result=model.S_resume(data)
        print("search_result:",result)
    #     Redis_save(data,result)
        return app.make_response((result,200,{"Content-Type":"application/josn;charset=utf-8"}))
    except:
        return app.make_response(({"查询失败":"查询失败"},500,{"Content-Type":"application/josn;charset=utf-8"}))

if __name__=='__main__':
    app.config['JSON_AS_ASCII'] = False
    app.debug=True
    host = config.configer.get("server", "host")
    port = config.configer.get("server", "port")
    app.run(host=host,port=port,debug=False,threaded=True)
