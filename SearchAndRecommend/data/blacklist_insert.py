# 向elasticsearch插入输入
from elasticsearch import Elasticsearch
from elasticsearch import helpers
import pymysql
import time
import pymssql

# 连接ES
es = Elasticsearch(
    ['127.0.0.1'],
    port=9200
)

# 连接MySQL
# print("Connect to mysql...")
# mysql_db = "recruitment"
# m_conn = pymysql.connect(host='192.168.200.128', port=3306, user='root', passwd='zxl123456', db=mysql_db, charset="utf8")
# m_cursor = m_conn.cursor()

print("Connect to sql server...")
server = '127.0.0.1'
user = 'SA'
password = "Zxl123456"
database = "kunshan_base"
conn = pymssql.connect(server, user, password, database)
m_cursor = conn.cursor()


def gen():
    """使用生成器批量写入数据"""
    print("开始执行生成器")
    action = ({
        "_index": "real_res",
        "_type": "res_info",
        "_routing": "fu_res",
        "_source": {
            "resume_relation": {
                "name": "black_table",
                "parent": "person_list"
            },
            'PerID': line[1],
            'ComID': line[2],
            'ComName': line[3]
        }
    } for line in query_results)
    # 形成一个长度与查询结果数量相等的列表
    helpers.bulk(es, action, raise_on_error=True)

try:
    num_id = 0

    s = time.time()
    # 查询数据: 黑名单表
    sql = "select * from dbo.perBlackCom"
    # 这里假设查询出来的结果为 张三 26 北京
    m_cursor.execute(sql)
    query_results = m_cursor.fetchall()

    if not query_results:
        print("sql server查询结果为空 num_id=<{}>".format(num_id))
    else:
        # print(type(query_results))  # list 内为 tuple
        gen()
        e = time.time()
        print("写入耗时:{}s".format(e - s))
    num_id += 1

finally:
    m_cursor.close()
    conn.close()
    print("SQL Server connection close...")
