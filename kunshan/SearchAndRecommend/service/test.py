from elasticsearch import Elasticsearch
from elasticsearch import helpers
import pymysql
import time


if __name__ == '__main__':
    es = Elasticsearch(
        ['127.0.0.1'],
        port=9200
    )
    # es.delete_by_query(index='kunshan-pos',body={
    #     'query':{
    #         'match_all':{}
    #     }
    # })
    # a=es.search(index='kunshan-pos',doc_type="pos_info")
    # print(a)



