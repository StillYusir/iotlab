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
    sql = "select * from res "
    # 这里假设查询出来的结果为 张三 26 北京
    m_cursor.execute(sql)
    query_results = m_cursor.fetchall()

    if not query_results:
        print("MySQL查询结果为空 num_id=<{}>".format(num_id))

    else:
        actions = []
        for line in query_results:
        # 拼接插入数据结构
            action = {
                "_index": "Search-res",
                "_type": "res_info",
                "_source": {
                     "Resid": line[0],
                     "Perid": line[1],
                     "ResumeName": line[2],
                     "DoneRate": line[3],
                     "Realname": line[4],
                    "Sex": line[5],
                    "SexName": line[6],
                    "PhotoUrl": line[7],
                    "BirthDate": line[8],
                    "Marriage": line[9],
                     "MarriageName": line[10],
                     "WorkArea": line[11],
                    "WorkAreaName": line[12],
                     "HomeArea": line[13],
                    "HomeAreaName": line[14],
                     "Degree": line[15],
                    "DegreeName": line[16],
                     "WishJobType": line[17],
                     "WishArea": line[18],
                     "WishSalary": line[19],
                    "WishSalaryName": line[20],
                    "ExpItem": line[21],
                    "ExpSkill": line[22],
                      "ExpAddons": line[23],
                      "UpdateDate": line[24],
                    "BaseInfo": line[25],
                    "Age": line[26],
                     "WorkYear": line[27],
                    "BeginWorkDate": line[28]

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


