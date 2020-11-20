import datetime
import threading
import json

import pymysql
from SearchAndRecommend.static.class_hash import small_jobtype

# 连接MySQL
print("Connect to mysql...")
mysql_db = "recruitment"
m_conn = pymysql.connect(host='192.168.222.128', port=3306, user='root',
                         passwd='zxl123456', db=mysql_db, charset="utf8")
m_cursor = m_conn.cursor()


def get_small_pos_count():
    # 循环遍历数据库，查询每个小类中所包含的职位的数量，对应返回数量，并存储到字典中
    _list = []
    for jobtype in small_jobtype:
        sql = 'select count(*) from pos where JobType = ' + str(int(jobtype))
        m_cursor.execute(sql)
        count = m_cursor.fetchone()

        dic = dict()
        if jobtype in dic.keys():
            dic[jobtype].append(count[0])
        else:
            dic[jobtype] = count[0]
        _list.append(dic)
    #print(_list)
    jsontext = {"data": {}}
    for val in _list:
        for key, value in val.items():
            jsontext["data"][key] = value
    jsondata = json.dumps(jsontext, indent=4, separators=(",", ":"), ensure_ascii=False)
    f = open("../static/static_pos_count.json", "w")
    f.write(jsondata)
    f.close()

# 如果需要循环调用，就要添加以下方法
timer = threading.Timer(86400, get_small_pos_count)
timer.start()



# 获取现在时间
now_time = datetime.datetime.now()
# 获取明天时间
next_time = now_time + datetime.timedelta(days=+1)
next_year = next_time.date().year
next_month = next_time.date().month
next_day = next_time.date().day
# 获取明天2点时间
next_time = datetime.datetime.strptime(str(next_year) + "-" + str(next_month) + "-" + str(next_day) + " 02:00:00",
                                       "%Y-%m-%d %H:%M:%S")
# # 获取昨天时间
# last_time = now_time + datetime.timedelta(days=-1)

# 获取距离明天2点时间，单位为秒
timer_start_time = (next_time - now_time).total_seconds()
print(timer_start_time)

# 定时器,参数为(多少时间后执行，单位为秒，执行的方法)
timer = threading.Timer(timer_start_time, get_small_pos_count)
timer.start()

