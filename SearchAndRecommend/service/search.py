import sys
sys.path.append('/home/iotlab/Search/')
from elasticsearch import Elasticsearch
from SearchAndRecommend.common.SearchEntiy import Search_preprocess
from SearchAndRecommend.common import CleanData as cd
from SearchAndRecommend.service.Post_Process import PP
from SearchAndRecommend.service.convertMessage import areaExpansion, get_number
from SearchAndRecommend.service.keyword_fiter import Filter
import time
from datetime import datetime

es = Elasticsearch([{'host': '127.0.0.1', 'port': 8769}])
a = Search_preprocess()
path = '../dicts/sensitive_words_new.txt'


class ESearch():
    def completion(self, info):
        doc = {
            "suggest": {
                "my-suggest": {
                    "prefix": [],
                    "completion": {
                        "field": "KeyName",
                        "analyzer": "ik_max_word",
                        "skip_duplicates": "true",
                        "size": 10000
                    }
                }
            }
        }

        doc.get('suggest').get('my-suggest').get("prefix").append(info['keyword'])
        print(doc)
        res = es.search(index="keyword", doc_type='key_info', body=doc, size=10)
        res = PP().post_process_com(res)
        return res

    def S_Job(self, info):
        # 过滤info['keyword]之后再搜索，过滤前后不一致说明这条关键词没价值，不予收录
        Filter.parse(path)
        filter_keyword = Filter.filter(info['keyword'], "")
        exist_doc = {"query": {"bool": {"must": [
            {"match": {
                "KeyName.keyword": filter_keyword
            }}
        ]}}}
        analyze = {
            "analyzer": "ik_smart",
            "text": filter_keyword
        }
        key_res = es.search(index="keyword", doc_type="key_info", body=exist_doc)
        if filter_keyword == info['keyword']:
            if key_res["hits"]["total"] == 0:
                if 2 <= get_number(filter_keyword) <= 8:
                    print("新插入关键词")
                    Analyze = es.indices.analyze(index='keyword', body=analyze)
                    b = []
                    for j in Analyze.get('tokens'):
                        b.append(j.get('token'))
                    ana = ' '.join(b)
                    insert_keyword = {
                        "KeyName": filter_keyword,
                        "hits": 0,
                        "IsStop": 0,
                        "analyze": ana
                    }
                    es.index(index='keyword', doc_type='key_info', body=insert_keyword)
            else:
                print("已有此关键词")
                update_keyword = {
                    "query": {
                        "match": {
                            "KeyName.keyword": filter_keyword
                        }
                    },
                    "script": {
                        "source": "ctx._source.hits +=1"
                    }
                }
                es.update_by_query(index='keyword', doc_type='key_info', body=update_keyword)
                if key_res["hits"]["hits"][0]["_source"].get("KeyName") != key_res["hits"]["hits"][0]["_source"].get(
                        "analyze").replace(" ", ""):
                    info["keyword"] = key_res["hits"]["hits"][0]["_source"].get("analyze").replace(" ", "")
        # 用户传入参数不定，可能发生异常
        #  2100 > jobEndDate > current_time
        current_time = datetime.now().strftime("%Y-%m-%d")
        Custom_Field = a.FieldChange(info)
        doc = {
            "size": int(info['pageSize']),
            "from": int(info['pageSize'])*(int(info["pageIndex"])-1),
            "query": {
                "bool": {
                    "must": [{"range": {"JobEndDate": {"gte": current_time, "lte": '2100-01-01'}}}],
                    "must_not": [],
                    'should': []
                }
            },
            "sort": [
                {"OrderTime": {"order": "desc"}},
                {"_score": {"order": "desc"}},
                {"JobTopEndDate": {"order": "desc"}}
            ],
            "aggs": {"group_by_jobtype": {"terms": {"field": "JobType", "size": 20},
                    "aggs": {"group_by_jobtype_name": {"terms": {"field": "JobTypeName"}}}}}
        }
        salary = ['salaryLabel']
        keyword = ['keyword']
        must = ['JobSex', 'JobProperty', 'ComArea', 'JobType', 'JobWorkYears', 'JobDegree', 'ComScale', 'ComTrade',
                'Comproperty']
        area = ['JobArea']
        keys = list(Custom_Field.keys())
        # print(keys)
        for key in keys:
            if Custom_Field[key] != "":
                if key in salary:  # 月薪涵盖
                    try:
                        S_map = a.Map_salary(info['salaryLabel'])  ##薪水映射
                        jobPayMax, jobPayMin = int(S_map[0]), int(S_map[1])
                        print(jobPayMin, jobPayMax)
                        # 查询2-3k包含不限，要在must里面的添加should才能表示or
                        # doc.get('query').get('bool').get("must").append({"bool": {"should": [{"range":{"JobPayMin":{"gte":jobPayMin/1000,"lt":jobPayMax/1000}}},{"range": {"JobPayMax": {"gte": 0, "lte":0}}}]}})
                        doc.get('query').get('bool').get("must").append(
                            {"range": {"JobPayMin": {"gte": int(jobPayMin / 1000), "lt": int(jobPayMax / 1000)}}})
                        doc.get('query').get('bool').get("must_not").append({"match": {"JobPayMax": "0"}})
                    except:
                        print('未传入薪水')
                elif key in area:  # 区域涵盖
                    try:
                        area = areaExpansion(info[key])
                        doc.get('query').get('bool').get("must").append({"terms": {key: area}})
                    except:
                        doc.get('query').get('bool').get("must").append({"match": {key: info[key]}})
                elif key in keyword:  # 多字段匹配，权重分配
                    doc.get('query').get('bool').get("must").append(
                        {"query_string": {"fields": ["JobName^10", "ComName^0.5"], "query": info[key]}})
                elif key in must:
                    doc.get('query').get('bool').get("must").append({"terms": {key: [info[key]]}})
        print(doc)
        query = es.search(index="realpos", doc_type='doc', body=doc)
        res = PP().post_process_pos(query, info)
        return res

    def S_Resume(self, info):
        doc = {
            "query": {
                "bool": {
                    "must": [],
                    "must_not": [],
                    'should': []
                }
            },
            "sort": [
                {"_score": {"order": "desc"}},
                {"LoginNum": {"order": "desc"}}
            ]
        }
        # 映射，数据库没有age字段，只有birthday，没有工作经验字段，只有开始工作时间、结束工作时间
        workYear = ['minWorkYear', 'maxWorkYear']
        # 涵盖
        area = ['WorkArea', 'WishArea']
        sex = ['Sex']
        # 直接检索
        must = ['WishJob']
        # 范围
        salary = ['exceptedSalaryLabel']
        degree = ['minEdu', 'maxEdu']
        age = ['minAge', 'maxAge']
        Custom_Field = a.FieldChange_Res(info)
        keys = list(Custom_Field.keys())
        # 输入参数和查询数据库有多对一的关系，避免多次查询设置flag
        flag_degree, flag_age, flag_year = 0
        for key in keys:
            if Custom_Field[key] != "":
                if key in must:
                    doc.get('query').get('bool').get("must").append({"match": {key: info[key]}})
                elif key in sex:
                    sex = a.Map_sex(info[key])
                    doc.get('query').get('bool').get("must").append({"terms": {key: [info[key]]}})
                elif key in area:
                    try:
                        doc.get('query').get('bool').get("must").append({"terms": {key: areaExpansion(info[key])}})
                    except:
                        doc.get('query').get('bool').get("must").append({"match": {key: info[key]}})
                elif key in salary:
                    try:
                        S_map = a.Map_salary(info['exceptedSalaryLabel'])  ##薪水映射
                        jobPayMax, jobPayMin = int(S_map[0]), int(S_map[1])
                        print(jobPayMin, jobPayMax)
                        doc.get('query').get('bool').get("must").append(
                            {"range": {"WishSalaryMin": {"gte": int(jobPayMin / 1000), "lt": int(jobPayMax / 1000)}}})
                        doc.get('query').get('bool').get("must_not").append({"match": {"WishSalaryMax": "0"}})
                    except:
                        print('未传入薪水')
                elif key in degree and flag_degree == 0:
                    flag_degree = 1
                    if info['minEdu'] == "":
                        info['minEdu'] = 3401
                    elif info['maxEdu'] == "":
                        info['maxEdu'] = 3407
                    doc.get('query').get('bool').get("must").append(
                        {"range": {
                            "Degree": {"gte": int(info['minEdu']), "lte": int(info['maxEdu'])}}})
                elif key in age and flag_age == 0:
                    flag_age = 1
                    doc.get('query').get('bool').get("must").append(
                        {"range": {
                            'BirthDate': {"gte": int(time.asctime()[-4:]) - int(info['minAge']),
                                          "lte": int(time.asctime()[-4:]) - int(info['maxAge']),
                                          "format": "yyyy/MM/dd"}}})
                # TODO 2021-1-30 减去 2000-1-30等于？
                elif key in workYear and flag_year == 0:
                    flag_year = 1
                    doc.get('query').get('bool').get("must").append(
                        {"script": {"script": "doc['EndDate'].value - doc['BeginDate'].value>info[]"}}
                    )
        # 条件整理结束，生成最终doc
        es.search(index="real_res", doc_type='res_info', body=doc)

    def R_Job(self, info):
        try:
            info['JobArea'], info['JobType'] = self.FilterJob(info)
        except:
            print('未传入工作类型或工作地点')
        try:
            S_map = a.Map_salary(info['WishSalaryName'])  ####薪水映射
            jobPayMax, jobPayMin = str(S_map[0]), str(S_map[1])
            info['JobPayMax'], info['JobPayMin'] = jobPayMax, jobPayMin
        except:
            print('未传入薪水')
        doc = {
            "query": {
                "bool": {
                    "must": [],
                    'should': []
                }
            },
            'size': 20
        }
        should = ['JobArea', 'JobType', "JobSalary"]
        must = ['JobPayMax', 'JobPayMin', "JobSexName"]
        keys = list(info.keys())
        for key in keys:
            if key in should:
                doc.get('query').get('bool').get("should").append({"terms": {key: info[key]}})
            elif key in must:
                doc.get('query').get('bool').get("must").append({"terms": {key: info[key]}})
        print(doc)
        res = es.search(index="Search-pos", doc_type='pos_info', body=doc)
        return res

    def FilterJob(self, ResumeInfo):
        if len(ResumeInfo["WishJobType"]) >= 6:
            wishJobType = cd.CleanWishJobType(ResumeInfo["WishJobType"])
        else:
            wishJobType = list(ResumeInfo["WishJobType"])
        if len(ResumeInfo["WishArea"]) >= 7:
            wishArea = cd.CleanWishArea(ResumeInfo["WishArea"])
        else:
            wishArea = list(ResumeInfo["WishArea"])
        print(wishArea, wishJobType)
        return wishArea, wishJobType

    def R_Resume(self, info):
        try:
            info['WishArea'], info['WishJobType'] = info['JobArea'], info['JobType']
        except:
            print('未传入工作类型或工作地点')
        try:
            S_map = a.Map_salary(info['JobSalary'])  ####薪水映射
            jobPayMax, jobPayMin = str(S_map[0]), str(S_map[1])
            info['JobPayMax'], info['JobPayMin'] = jobPayMax, jobPayMin
        except:
            print('未传入薪水')
        doc = {
            "query": {
                "bool": {
                    "must": [],
                    'should': []
                }
            },
            "size": 20
        }

        should = ["WishJobType", 'WishArea']
        must = ['WishSalary', 'JobPayMax', 'JobPayMin']
        keys = list(info.keys())
        for key in keys:
            if key in should:
                doc.get('query').get('bool').get("should").append({"match": {key: info[key]}})
            elif key in must:
                doc.get('query').get('bool').get("must").append({"match": {key: info[key]}})
        print(doc)
        res = es.search(index="Search-res", doc_type='res_info', body=doc)
        return res


if __name__ == '__main__':
    pass
#     doc={
#         "query":{
#         "bool":{
#         "must":[],
#         'should':[]
#
#         }
#     }
# }
# dicts={}
# should=[]
# must=[]
# for key in dicts.keys():
#     if key in should:
#         doc.get("bool").get("should").append({"match":{key:dicts[key]}})
#     else:
#         doc.get("bool").get("must").append({"match": {key: "123"}})
# print(doc.get("bool").get("must"))
# print(doc.__str__())
# doc.get('bool').get('must').append({"match": {"jobName": "工程师"}})
# # doc.get('bool').get('should').append({"match": {"jobSexName": "不限"}})
# doc.get('query').get('bool').get("must").append({"match": {"jobName": "工程师"}})
# doc.get('query').get('bool').get("should").append({"match": {"jobSexName": "不限"}})
# # print(doc)
# # print(doc.get("bool").get("must"))
# a=es.search(index="Search",doc_type='per_info',body=doc)
# print(a)
# body={'query':{'bool': {'must': [{'match': {'jobName': '工程师'}}]}}}
# a=es.search(index="Search", doc_type='per_info', body=body)
# print(a)
# aa={'jobName':''}
# print(aa.get())
# print(aa.get("jobName"))
# bb={'jobSexName':"不*"}
# s=Search(using=es,index="Search").update_from_dict({"query": {"multi-match": aa}})
# s=Search(using=es,index="Search").query("",**bb)
#
# print(s.execute())

# ms=MultiSearch(index='Search')
#  ms =ms.add(Search(using=es,index="Search").filter("match",jobName=aa.get("jobName")))
#  ms =ms.add(Search(using=es,index="Search").filter("match", jobSexName=bb.get("jboSexName")))
#

# a= Q('bool', must=[Q('match', jobName=aa.get("enttype_code")), Q('match', jobSexName=aa.get("jobSexName"))],should=[Q('term',jobName='python')])
#  print(s.query(ms).execute())
