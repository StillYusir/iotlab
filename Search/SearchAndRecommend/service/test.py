from elasticsearch import Elasticsearch
from elasticsearch import helpers
import pymysql
import time
import synonyms


if __name__ == '__main__':
    es = Elasticsearch(
        ['127.0.0.1'],
        port=9200
    )

    # parameter='abcsda$'
    # try:
    #     int(parameter)
    # except:
    #     parameter=1
    # print(parameter)

    # print(synonyms.nearby('JAVA'))

    # es.delete_by_query(index='Search-pos',body={
    #     'query':{
    #         'match_all':{}
    #     }
    # })
    # a=es.search(index='Search-pos',doc_type="pos_info")
    # print(a)



