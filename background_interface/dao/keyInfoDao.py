from background_interface.utils.confReader import conf
from elasticsearch import Elasticsearch
import time
import os

class KeyInfoDao:
    def __init__(self):
        host = conf["host"]
        port = conf["port"]
        self.es = Elasticsearch([{'host': host, 'port': port}])

    def query_data_by_page(self, key_name, curr_page, page_size):
        if curr_page < 1:
            return "page must greater or equal to one"
        if page_size < 1:
            return "page must greater or equal to one"
        from_ = int(curr_page - 1) * page_size
        body = {
            "from": from_, "size": page_size,
            "query": {
                "match": {
                    "KeyName.text": key_name.strip()
                }
            }
        }
        if key_name.strip() == '' or key_name is None or not key_name:
            body = {
                "from": from_, "size": page_size,
                "query": {"match_all": {}}
            }
        origin_res = self.es.search(index='keyword', doc_type='key_info', body=body)
        res = {"data":{"reslist":[{"recordId":"","KeyName":"","hits":"","IsStop":"","analyze":""}]}}
        if origin_res["hits"]["total"] == 0:
            # print('hists total', origin_res['hits']['total'])
            return "NONE"
        else:
            res.get('data')['total_pages'] = int((origin_res["hits"]["total"] + page_size -1) / page_size)
            for index, JSON in enumerate(origin_res['hits']['hits']):
                res.get('data')['reslist'][index]['recordId'] = JSON["_id"]
                res.get('data')['reslist'][index]['KeyName'] = JSON["_source"]["KeyName"]
                res.get('data')['reslist'][index]['hits'] = JSON["_source"]["hits"]
                res.get('data')['reslist'][index]['IsStop'] = JSON["_source"]["IsStop"]
                res.get('data')['reslist'][index]['analyze'] = JSON["_source"]["analyze"]
                if index != (page_size - 1):
                    res.get('data')['reslist'].append({"recordId":"","KeyName":"","hits":"","IsStop":"","analyze":""})
                else:
                    break
            return res

    def update_isStop(self, recordId, isStop):
        if isStop not in [0, 1]:
            return "parameter invalid, is stop should be int 0 or int 1"
        body = '''{"doc": {"IsStop": "%s"}}''' % (isStop)
        print("body is {}".format(body))
        # 文档不存在会报错。
        self.es.update(index="keyword", doc_type='key_info', id=recordId, body=body)
        return True

    def update_analyze(self, recordId, analyze):
        body = '''{"doc": {"analyze": "%s"}}''' % (analyze)
        print("body is {}".format(body))
        self.es.update(index="keyword", doc_type='key_info', id=recordId, body=body)
        return True

    def get_doc_by_id(self, recorId):
        body = {
            "query": {
                "bool": {
                    "filter": {
                        "term": {
                            "_id": recorId
                        }
                    }
                }
            }
        }
        res = self.es.search(index='keyword', doc_type='key_info', body=body)
        return res

host = conf["host"]
port = conf["port"]
keyInfoDao = KeyInfoDao()


if __name__ == '__main__':
    print(KeyInfoDao.query_data_by_page(KeyInfoDao,"", 1, 2))
    print(KeyInfoDao().update_isStop("fnUNPXcBpOF4N_9ZQYHg", "1"))
    print(KeyInfoDao().update_analyze("fnUNPXcBpOF4N_9ZQYHg", "苏州兆鑫驰智能科技有限公"))

    time.sleep(3)
    print(KeyInfoDao().query_data_by_page("", 1, 2))
    print(KeyInfoDao().get_doc_by_id("fnUNPXcBpOF4N_9ZQYHg"))

