import json


class IndexView():
    """类别分类"""
    def init_get_pos_count(self):
        with open("../static/static_pos_count.json", 'r') as f:
            temp = json.loads(f.read())
            val = temp['data']
            val_list = []
            for key0, value in val.items():
                dict11 = {}
                temp_value = 0
                if int(value) > temp_value:
                    temp_value = int(value)
                    dict11["jobType"] = str(key0)
                    dict11["jobNum"] = temp_value
                    val_list.append(dict11)
            return val_list

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
