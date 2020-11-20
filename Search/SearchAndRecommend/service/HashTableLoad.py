import json


class IndexView():
    """类别分类"""
    def get_pos_count(num2):
        '''查询小类中 所包含的职位的数量'''
        num2 = int(num2)
        with open("../static/static_pos_count.json", 'r') as f:
            temp = json.loads(f.read())
            val = temp['data']
            # print("val:",val)
        for key, value in val.items():
            if key == str(num2):
                count = val[key]
                return count

    # def get_pos(num2):
    #     '''查询小类中包含的职位，并进行分页返回'''
    #     sql = 'select * from pos where JobType = ' + num2
    #     m_cursor.execute(sql)
    #     pos_list = m_cursor.fetchall()
    #     # print(type(pos_list))  # tuple
    #     return pos_list

    # m_cursor.close()
    # m_conn.close()
    # print("MySQL connection close...")

    def get_area_count(num):
        '''查询省市中  所有区、镇 的数量'''
        with open("../static/static_area_count.json", 'r') as f:
            temp = json.loads(f.read())
            val = temp['data']
            # print("val:",val)
        for key, value in val.items():
            if key == str(num):
                count = val[key]
                return count
