import json
import traceback
from datetime import datetime


def tiqu_small_class_index():
    with open("../data/job.json", 'r') as f1:
        temp = json.loads(f1.read())
        val = temp['job_categories']
        small_list_index = []
        for index in val.values():
            small_list_index.append(int(index))
    f1.close()

    with open("../static/static_combine_job.json", 'r', encoding='utf-8') as f2:
        dic = dict()
        _list = []
        i = 0
        while True:
            line = f2.readline()  # 逐行读取
            line = line.replace("\n", "").replace("\\", "").replace("\x1a", "").replace('\x01', '').replace('\x16', '')
            if not line:  # 到 EOF，返回空字符串，则终止循环
                break

            try:
                i += 1
                line = json.loads(line)
            except Exception as e:
                # print(e.__traceback__.tb_lineno)  # 发生异常的代码所在的行数
                traceback.print_exc(file=open('../Exception/traceback_INFO.txt', 'a+'))
                f3 = open("../Exception/traceback_INFO.txt", "a+")     # 将抛出异常的源文件所对应的行号以及详细异常信息保存在log文件中
                f3.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S")+":"+"上面错误是源文件中的第{}行".format(i)+"\n")
                f3.close()
                continue
            print("第{}行".format(i))    # 源文件中起始行号为 1
            print(line)
            for jobtype in small_list_index:
                if int(line["JobType"]) == jobtype:
                    if jobtype in dic.keys():
                        dic[jobtype] = int(dic[jobtype]) + 1
                    else:
                        dic[jobtype] = 1
        _list.append(dic)
    f2.close()

    # print(_list)
    jsontext = {"data": {}}
    for val in _list:
        for key, value in val.items():
            jsontext["data"][key] = value
    jsondata = json.dumps(jsontext, indent=4, separators=(",", ":"), ensure_ascii=False)
    f = open("../static/static_pos_count.json", "w", encoding='utf-8')
    f.write(jsondata)
    f.close()

if __name__ == '__main__':
    tiqu_small_class_index()
