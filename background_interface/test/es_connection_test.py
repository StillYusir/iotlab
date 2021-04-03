from elasticsearch import Elasticsearch

es=Elasticsearch([{'host': '139.196.146.45', 'port': 8769}])


def completion():
    # doc = {
    #     "suggest": {
    #         "my-suggest": {
    #             "prefix": [],
    #             "completion": {
    #                 "field": "JobName",
    #                 "analyzer": "ik_max_word",
    #                 "skip_duplicates": "true"
    #             }
    #         }
    #     }
    # }
    #
    # doc.get('suggest').get('my-suggest').get("prefix").append(info['keyword'])
    # print(doc)
    doc={
        "query": {"match_all": {}},
        "size": 99999
    }
    res = es.search(index='keyword',doc_type='key_info',body=doc, size=1000)
    print(res)
    # p = PP()
    # res = p.post_process_com(res)
    return res

completion()

