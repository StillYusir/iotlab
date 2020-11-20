from flask import Flask, request
import json
import sys
sys.path.append('/home/iotlab/Search/')

from SearchAndRecommend.dao import config
from SearchAndRecommend.service.search import ESearch
from SearchAndRecommend.service.redis_server import GetInfo,Redis_save

app=Flask(__name__)
model=ESearch()

@app.route('/completion/result',methods=['POST'])
def com_service():
    data = json.loads(request.data.decode("utf-8"))
    result=model.completion(data)
    return app.make_response((result, 200, {"Content-Type": "application/josn;charset=utf-8"}))

@app.route('/search/pos-result',methods=['POST'])
def pos_service():
    data=json.loads(request.data.decode("utf-8"))
    data_copy=json.loads(request.data.decode("utf-8"))
    #redis 搜索
    result=GetInfo(data)
    if result !=None:
        print('调用缓存')
        return app.make_response((result,200,{"Content-Type":"application/josn;charset=utf-8"}))
    else:
        print('无缓存')
        result=model.S_Job(data)
        Redis_save(data_copy,result)
        return app.make_response((result,200,{"Content-Type":"application/josn;charset=utf-8"}))

@app.route('/search/res-result',methods=['POST'])
def res_service():
    data = json.loads(request.data.decode("utf-8"))
    result=GetInfo(data)
    if result !=None:
        print('调用缓存')
        return app.make_response((result,200,{"Content-Type":"application/josn;charset=utf-8"}))
    else:
        print('无缓存')
        result=model.S_Resume(data)
        Redis_save(data,result)
        return app.make_response((result,200,{"Content-Type":"application/josn;charset=utf-8"}))

@app.route('/recommend/pos-result',methods=['POST'])
def RecJob_service():
    data = json.loads(request.data.decode("utf-8"))
    result=GetInfo(data)
    if result !=None:
        print('调用缓存')
        return app.make_response((result,200,{"Content-Type":"application/josn;charset=utf-8"}))
    else:
        print('无缓存')
        result=model.R_Job(data)
        Redis_save(data,result)
        return app.make_response((result,200,{"Content-Type":"application/josn;charset=utf-8"}))

@app.route('/recommend/res-result',methods=['POST'])
def RecRes_service():
    data = json.loads(request.data.decode("utf-8"))
    result=GetInfo(data)
    if result !=None:
        print('调用缓存')
        return app.make_response((result,200,{"Content-Type":"application/josn;charset=utf-8"}))
    else:
        print('无缓存')
        result=model.R_Resume(data)
        Redis_save(data,result)
        return app.make_response((result,200,{"Content-Type":"application/josn;charset=utf-8"}))

@app.route('/similar/pos-result',methods=['POST'])
def Pos_service():
    data=json.loads(request.data.decode("utf-8"))
    #redis 搜索
    result=GetInfo(data)
    print(result)
    if result !=None:
        print('调用缓存')
        return app.make_response((result,200,{"Content-Type":"application/josn;charset=utf-8"}))
    else:
        print('无缓存')
        result=model.S_Job(data)
        Redis_save(data,result)
        return app.make_response((result,200,{"Content-Type":"application/josn;charset=utf-8"}))

@app.route('/similar/res-result',methods=['POST'])
def Res_service():
    data = json.loads(request.data.decode("utf-8"))
    result=GetInfo(data)
    if result !=None:
        print('调用缓存')
        return app.make_response((result,200,{"Content-Type":"application/josn;charset=utf-8"}))
    else:
        print('无缓存')
        result=model.S_Resume(data)
        Redis_save(data,result)
        return app.make_response((result,200,{"Content-Type":"application/josn;charset=utf-8"}))

if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    app.debug=True
    host= config.configer.get('server', 'host')
    port= config.configer.get('server', 'port')
    app.run(host=host,port=port,threaded=True)



