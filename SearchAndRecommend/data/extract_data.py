import json
import pymysql

print("Connect to mysql...")
mysql_db = "recruitment"
m_conn = pymysql.connect(host='127.0.0.1', port=3306, user='root',
                         passwd='root', db=mysql_db, charset="utf8")
m_cursor = m_conn.cursor()


def tiqu_small_class_index():
    with open("./job.json", 'r') as f:
        temp = json.loads(f.read())
        val = temp['job_categories']

        small_list_index = []
        for index in val.values():
            small_list_index.append(int(index))

       # print(small_list_index)  # list
        _list = []
        for jobtype in small_list_index:
            sql = 'select count(*) from position where JobType = ' + str(jobtype)
            m_cursor.execute(sql)
            count = m_cursor.fetchone()

            dic = dict()
            if jobtype in dic.keys():
                dic[jobtype].append(count[0])
            else:
                dic[jobtype] = count[0]
            _list.append(dic)
        # print(_list)
        jsontext = {"data": {}}
        for val in _list:
            for key, value in val.items():
                jsontext["data"][key] = value
        jsondata = json.dumps(jsontext, indent=4, separators=(",", ":"), ensure_ascii=False)
        f = open("../static/static_pos_count.json", "w")
        f.write(jsondata)
        f.close()

if __name__ == '__main__':
    tiqu_small_class_index()