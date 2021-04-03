#向elasticsearch插入输入
from elasticsearch import Elasticsearch
from elasticsearch import helpers
import pymysql
import time

# 连接ES
es = Elasticsearch(
    ['127.0.0.1'],
    port=9200
)


# 连接MySQL
print("Connect to mysql...")
mysql_db = "recruitment"
m_conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='001369', db=mysql_db, charset="utf8")
m_cursor = m_conn.cursor()



try:
    num_id = 0

    s = time.time()
    # 查询数据
    sql = "select * from keyword "
    # 这里假设查询出来的结果为 张三 26 北京
    m_cursor.execute(sql)
    query_results = m_cursor.fetchall()
    print(query_results)
    if not query_results:
        print("MySQL查询结果为空 num_id=<{}>".format(num_id))
    else:
        actions = []
        for line in query_results:
        # 拼接插入数据结构
            action = {
                "_index": "keyword",
                "_type": "key_info",
                "_source": {
                    'id': line[0],
                    'KeyName': line[1],
                    'hits': int(line[2]),
                    'QP': line[3],
                    'JP': line[4],
                    'ZWS': line[5],
                    'ZWSNow': line[6],
                    'upTime': line[7],
                    'IsCom':line[8]

                }
        }
            # 形成一个长度与查询结果数量相等的列表
            actions.append(action)
        # 批量插入
        a = helpers.bulk(es, actions)
        e = time.time()
        print("{} {}s".format(a, e-s))
    num_id += 1

finally:
    m_cursor.close()
    m_conn.close()
    print("MySQL connection close...")


