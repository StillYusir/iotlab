from elasticsearch import Elasticsearch
from SearchAndRecommend.control.SearchEntiy import Search_preprocess
from SearchAndRecommend.service import CleanData as cd
from SearchAndRecommend.service.Post_Process import PP
import json


es=Elasticsearch([{'host': '127.0.0.1', 'port': 8769}])

a=Search_preprocess()


class ESearch():
    def completion(self,info):
        doc={
                    "suggest": {
                        "my-suggest": {
                            "prefix": [],
                            "completion": {
                                "field": "JobName",
                                "analyzer": "ik_max_word",
                                "skip_duplicates": "true"
                            }
                        }
                    }
                }

        doc.get('suggest').get('my-suggest').get("prefix").append(info['keyword'])
        print(doc)
        res = es.search(index="position", doc_type='pos_info', body=doc,size=10)
        p = PP()
        res=p.post_process_com(res)
        return res

    def S_Job(self,info):
        # Search_dict=a.make_dict(info)
        #用户传入参数不定，可能发生异常
        Custom_Field=a.FieldChange(info)
        doc = {
            "query": {
                "bool": {
                    "must": [],
                    'should': []
                }
            }
        }
        salary = ['salaryLabel']
        keyword=['keyword']
        should=['JobLight','JobTypeName']
        must=['JobArea', 'JobSex','JobProperty',
              'ComEmployee','JobWorkYears','JobDegree',
              'JobType','JobArea']
        keys=list(Custom_Field.keys())
        # print(keys)
        for key in keys:
            if Custom_Field[key]!="":
                if key in salary:
                    try:
                        S_map = a.Map_salary(info['salaryLabel'])  ####薪水映射
                        jobPayMax, jobPayMin = str(S_map[0]), str(S_map[1])
                        print(jobPayMin, jobPayMax)
                        doc.get('query').get('bool').get("must").append({"range":{"JobPayMin":{"gte":jobPayMin,"lt":jobPayMax}}})
                    except:
                        print('未传入薪水')
                elif key in keyword:
                    doc.get('query').get('bool').get("should").append({"match": {'JobName': info[key]}})
                    doc.get('query').get('bool').get("should").append({"match": {'ComName': info[key]}})
                elif key in must:
                    doc.get('query').get('bool').get("must").append({"match": {key: info[key]}})
        print(doc)
        res = es.search(index="position2", doc_type='pos_info', body=doc,size=1000)
        p = PP()
        res = p.post_process_pos(res,info)
        # if Custom_Field['keyword']!="":
        # 类别数量
        # dicts = convertMessage.statisticalQuantity(res)
        # type=[]
        # print(dicts)
        # for k, v in dicts.items():
        #     type.append([k, v[-1]['count']])
        # print(type)
        # return res
            # print(count)
        # res=json.dumps(post_process(res), ensure_ascii=False, indent=4)
        return res

    def S_Resume(self,info):
        #TODO 简历表中应加WorkYears 3501,WishJobType,WishArea--text
        try:
            W_map = a.Map_years(info["WorkYear"])  ####映射过程
            info['WorkYear'] = W_map
        except:
            print('未传入工作经验')
        #TODO 此处应该优化映射,搜索本科 是只要本科还是本科及以上

        doc = {
            "query": {
                "bool": {
                    "must": [],
                    'should': []
                }
            }
        }

        should =['ExpSkill','ExpAddons']
        must=['DegreeName','WishSalaryName','WishSalary','Age',
              'WorkYear','ResumeName','SexName','WishJobType','WishArea',
              'WorkArea','WorkAreaName','Perid','Resid']
        keys = list(info.keys())
        # print(keys)
        for key in keys:
            if key in should:
                doc.get('query').get('bool').get("should").append({"match": {key: info[key]}})
            elif key in must:
                doc.get('query').get('bool').get("must").append({"match": {key: info[key]}})
        # print(doc)
        res = es.search(index="Search-res", doc_type='res_info', body=doc)
        return res

    def R_Job(self,info):
        #传入WishJobType和，WishArea，WishSalary
        #TODO 目前职位表没有Salary2304类映射,简历表WishArea7位，
        # 但职位表JobArea8位，无法对应起来. 补上性别。

        try:
            info['JobArea'],info['JobType']=self.FilterJob(info)
        except:
            print('未传入工作类型或工作地点')
        try:
            S_map = a.Map_salary(info['WishSalaryName'])####薪水映射
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
            'size':20
        }
        should=['JobArea','JobType',"JobSalary"]
        must=['JobPayMax','JobPayMin',"JobSexName"]
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
        print(wishArea,wishJobType)
        return wishArea, wishJobType

    #TODO WishArea和WishJobType可能需要换一种mapping格式
    def R_Resume(self,info):
        try:
            info['WishArea'],info['WishJobType']=info['JobArea'],info['JobType']
        except:
            print('未传入工作类型或工作地点')
        try:
            S_map = a.Map_salary(info['JobSalary'])####薪水映射
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
            "size":20
                }
        
        should = ["WishJobType",'WishArea']
        must = ['WishSalary','JobPayMax','JobPayMin']
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
    # doc.get('bool').get('should').append({"match": {"jobSexName": "不限"}})
    doc.get('query').get('bool').get("must").append({"match": {"jobName": "工程师"}})
    doc.get('query').get('bool').get("should").append({"match": {"jobSexName": "不限"}})
    # print(doc)
    # print(doc.get("bool").get("must"))
    a=es.search(index="Search",doc_type='per_info',body=doc)
    print(a)
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



