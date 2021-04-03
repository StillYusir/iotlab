from elasticsearch import Elasticsearch
import json
import jieba
import re
import copy

es = Elasticsearch([{'host': '127.0.0.1', 'port': 9200}])

res = es.search(index="pos2", doc_type='pos_info', size=1000)


# res = json.dumps(res, ensure_ascii=False, indent=4)
# print(res)

# 保证2-8字
def get_number(char):
    count = 0
    for item in char:
        if 0x4E00 <= ord(item) <= 0x9FA5:
            count += 1
    return count


jobList = []
comList = []
keywords = []


# 全量收录
def key_words():
    for i in range(len(res['hits']['hits'])):
        # 增量收录
        element = dict()
        # 公司名收录
        comName = res['hits']['hits'][i]['_source']['ComName']
        if comName not in comList:
            element["KeyName"] = comName
            element["hits"] = 0
            element["IsStop"] = 0
            element["analyze"] = ""
            keywords.append(copy.deepcopy(element))
            comList.append(comName)

        # 职位名筛选
        jobName = res['hits']['hits'][i]['_source']['JobName']
        sss = jobName
        ss = re.sub(u"\\（.*?\\）|\\(.*?\\)|\\【.*?\\】：|\\{.*?\\}|\\[.*?\\]", "", sss)
        s = ss.replace("急招", "")
        if s.encode('utf-8').isalpha():
            str = ""
            for ss in s:
                if ss.isupper():
                    str += ' '
                str += ss
        else:
            str = ""
            for ss in s:
                if ss == '—' or ss == ' ' or ss == '~' or ss == '-' or ss == '(' or ss == '（':
                    break
                else:
                    str += ss
        # print(str)

        # 职位名分词收录
        seg_list = jieba.cut(str)
        result = ' '.join(seg_list)
        # print(jobid)
        # print(result)
        job_key = result.split(' ')
        for key in job_key:
            if key != "" and key not in jobList and get_number(key) >= 2 and get_number(key) <= 8:
                element["KeyName"] = key
                element["hits"] = 0
                element["IsStop"] = 0
                element["analyze"] = ""
                keywords.append(copy.deepcopy(element))
                jobList.append(key)

    return keywords


# key_words = key_words()
# keywords = json.dumps(key_words, ensure_ascii=False, indent=4)
# print(keywords)




# 增量收录
def key_incream(info):
    for i in len(info):
        # 职位名筛选
        element={}
        jobName = info[i]['JobName']
        sss = jobName
        ss = re.sub(u"\\（.*?\\）|\\(.*?\\)|\\【.*?\\】：|\\{.*?\\}|\\[.*?\\]", "", sss)
        s = ss.replace("急招", "")
        if s.encode('utf-8').isalpha():
            str = ""
            for ss in s:
                if ss.isupper():
                    str += ' '
                str += ss
        else:
            str = ""
            for ss in s:
                if ss == '—' or ss == ' ' or ss == '~' or ss == '-' or ss == '(' or ss == '（':
                    break
                else:
                    str += ss
        # print(str)

        # 职位名分词收录
        seg_list = jieba.cut(str)
        result = ' '.join(seg_list)
        # print(jobid)
        # print(result)
        job_key = result.split(' ')
        for key in job_key:
            if key != "" and key not in jobList and get_number(key) >= 2 and get_number(key) <= 8:
                element["KeyName"] = key
                element["hits"] = 0
                element["IsStop"] = 0
                element["analyze"] = ""
                keywords.append(copy.deepcopy(element))
                jobList.append(key)
    return keywords