# -*- coding: utf-8 -*-
import json
import os
import pickle

import requests
import time
from datetime import datetime
import sys
import _ctypes
import re
import traceback

sys.path.append('/home/iotlab/Search/')


def timestamp(now_time):
    c = str(time.localtime()[1] + time.localtime()[2] + time.localtime()[3] + time.localtime()[4] + time.localtime()[5])
    if int(c) < 100 and int(c) > 0:
        a = now_time.strftime("%Y-%m-%dT%H:%M:%S.0")
    else:
        a = now_time.strftime("%Y-%m-%dT%H:%M:%S.")
    b = a + c
    return b


def extract_and_combine_dict(dic):
    '''
    list1 = []
    i = 0
    for com in dic['ComList']:
        #com["ComID1"] = com.pop("ComID")
        for job in dic['JobList'][i:-1]:
            #job.update({"ComID2": job.pop("ComID")})
            dict11 = dict(com, **job)
            list1.append(dict11)
            i += 1
            break
    #list1.append(dict(dic['ComList'][-1], **dic['JobList'][-1]))
    '''

    list1 = []
    for com in dic["ComList"]:
        if com.get("ComID"):
            for job in dic["JobList"]:
                if job.get("ComID") and com["ComID"] == job["ComID"]:
                    dict11 = dict(com, **job)
                    list1.append(dict11)
    for dic in list1:
        dic["JobDesc"] = dic["JobDesc"].replace('\n', '').replace('\r', '').replace('\t', '').replace(
            '\\', '-') \
            .replace('"', '').replace('\b', '').replace('?', '').replace('“', '').replace('', '').replace('\x1a', '') \
            .replace('\x01', '').replace('\x16', '')
        dic["ComTradeName"] = dic["ComTradeName"].replace('\n', '').replace('\r', '')
        dic["Address"] = dic["Address"].replace('#', '').replace('/', '或').replace('\n', '').replace('\r', '').replace(
            ' ', '').replace('\t', '')
        dic["ComName"] = dic["ComName"].replace('\t', '').replace('\n', '').replace('\r', '').replace(' ', '').replace(
            '\b', '')
        dic["ComAreaName"] = dic["ComAreaName"].replace('\t', '').replace('\n', '').replace('\r', '').replace(' ',
                                                                                                              '').replace(
            '\b', '')
        dic["ComTradeName"] = dic["ComTradeName"].replace('\t', '').replace('\n', '').replace('\r', '').replace(' ',
                                                                                                                '').replace(
            '\b', '')
        dic["JobAddress"] = dic["JobAddress"].replace('\t', '').replace('\n', '').replace('\r', '').replace(' ',
                                                                                                            '').replace(
            '\b', '')
        dic["JobLight"] = dic["JobLight"].replace('\t', '').replace('\n', '').replace('\r', '').replace(' ',
                                                                                                        '').replace(
            '\b', '')
        dic["JobTypeName"] = dic["JobTypeName"].replace('\t', '').replace('\n', '').replace('\r', '').replace(' ',
                                                                                                              '').replace(
            '\b', '')
        dic["JobName"] = dic["JobName"].replace('\t', '').replace('\n', '').replace('\r', '').replace(' ', '').replace(
            '\b', '').replace('0"', '').replace('\\','-')

        if dic.get("JobType") and dic["JobType"] == '0':
            dic["JobType"] = re.sub(r"0", "219999", dic["JobType"])
            dic["JobTypeName"] = "其他职位"


    jsondata = json.dumps(OneDictPerLine(list1), cls=MyEncoder, ensure_ascii=False)

    with open("../static/static_combine_job.json", "w") as f:
        f.write(jsondata)
        f.flush()
        f.close()
    return len(list1)

    # # pickle 读写文件操作
    # with open("../static/static_combine_job.json", "wb") as f2:
    #     pickle.dump(jsondata, f2)
    #     f2.close()


class OneDictPerLine(object):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        if not isinstance(self.value, list):
            return repr(self.value)
        else:  # Sort the representation of any dicts in the list.
            reps = ("{{{}}}".format(", ".join(
                ('"{}":"{}"'.format(k, v) for k, v in sorted(v.items()))
            )) if isinstance(v, dict)
                    else
                    repr(v) for v in self.value)
            # return '[' + ',\n'.join(reps) + ']'
            return '\n'.join(reps)


def di(obj_id):
    """ Reverse of id() function. """
    return _ctypes.PyObj_FromPtr(obj_id)


class MyEncoder(json.JSONEncoder):
    FORMAT_SPEC = "@@{}@@"
    regex = re.compile(FORMAT_SPEC.format(r"(\d+)"))

    def default(self, obj):
        return (self.FORMAT_SPEC.format(id(obj)) if isinstance(obj, OneDictPerLine)
                else super(MyEncoder, self).default(obj))

    def encode(self, obj):
        format_spec = self.FORMAT_SPEC  # Local var to expedite access.
        json_repr = super(MyEncoder, self).encode(obj)  # Default JSON repr.

        # Replace any marked-up object ids in the JSON repr with the value
        # returned from the repr() of the corresponding Python object.
        for match in self.regex.finditer(json_repr):
            id = int(match.group(1))
            # Replace marked-up id with actual Python object repr().
            json_repr = json_repr.replace(
                '"{}"'.format(format_spec.format(id)), repr(di(id)))

        return json_repr


def full_synchronization():
    t = timestamp(datetime.now())
    url = 'http://yqcdata.kshr.com.cn/yqc.aspx'
    params = {"fun": "yqc_all", "t": t}
    reqst = requests.get(url, params=params)
    # print(reqst)   #<Response [200]>
    # print('type_dic:',type(reqst))  # type_dic: <class 'requests.models.Response'>
    reqst.encoding = reqst.apparent_encoding
    length = extract_and_combine_dict(reqst.json())
    print("list1的长度为：",length)
    print("全量存储成功！")
