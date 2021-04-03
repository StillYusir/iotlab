import pyodbc
from utils.confReader import conf
import json
from elasticsearch import Elasticsearch
import datetime
from service.ResumeMapperProperties import mp
from utils.date_match import calculate_days


class ResumeDao(object):
    def __init__(self):
        self.host_sql = conf["host_sql"]
        self.user_sql = conf["user_sql"]
        self.pwd_sql = conf["pwd_sql"]
        self.cur1 = self.__GetConnect('hrPer')
        self.cur2 = self.__GetConnect('hrCom')
        host_es = conf['host_es']
        port_es = conf['port_es']
        self.es = Elasticsearch([{'host': host_es, 'port': port_es}])

    def __GetConnect(self, db):
        # ubuntu16.04服务器：DRIVER={/opt/microsoft/msodbcsql17/lib64/libmsodbcsql-17.7.so.2.1}
        config = 'DRIVER={/opt/microsoft/msodbcsql17/lib64/libmsodbcsql-17.7.so.2.1};SERVER=' + self.host_sql + ',' + '1433;DATABASE=' + db + ';UID=' + \
                 self.user_sql + ';PWD=' + self.pwd_sql
        self.conn = pyodbc.connect(config)
        cur = self.conn.cursor()
        # print('连接%s:success!'%db)
        if not cur:
            raise (NameError, "连接数据库失败")
        else:
            return cur

    # 投递过滤
    def filter_deliver_list(self, ComID, deliver_flag):
        abandon_deliverResid = []
        if deliver_flag == '1':
            sql = 'SELECT ResID FROM ComResumeInterview where ComID = %s' % ComID
            self.cur2.execute(sql)
            cur_fetchall = self.cur2.fetchall()
            for index, i in enumerate(cur_fetchall):
                abandon_deliverResid.append(cur_fetchall[index][0])
        if deliver_flag == '0':
            return []
        print('投递表查询成功')
        return abandon_deliverResid

    # 下载过滤
    def filter_download_list(self, ComID, download_flag):
        ababdon_downloadResid = []
        if download_flag == '1':
            sql = 'SELECT ResID FROM ComResumeDownload where ComID = %s' % ComID
            self.cur2.execute(sql)
            cur_fetchall = self.cur2.fetchall()
            for index, i in enumerate(cur_fetchall):
                ababdon_downloadResid.append(cur_fetchall[index][0])
        if download_flag == '0':
            return []
        print('下载表查询成功')
        return ababdon_downloadResid

    # 区分 未下载和已下载简历
    def differ_download_list(self, present_resid, ComID):
        sql_res = []  # 已下载的简历（大）
        sql = """select ResID from ComResumeDownload where ComID = {}""".format(ComID)
        self.cur2.execute(sql)
        cur_fetchall = self.cur2.fetchall()
        for index, i in enumerate(cur_fetchall):
            sql_res.append(cur_fetchall[index][0])
        has_not_download = set(present_resid).difference(set(sql_res))  # 未下载
        has_download = set(present_resid).difference(set(has_not_download))  # 已下载
        return has_download, has_not_download

    def filter_blackList(self, ComID):
        """通过ComID对黑名单表的过滤"""
        abandon_blacklistPerID = []
        sql = 'SELECT PerID from perBlackCom where ComID = %s' % ComID
        self.cur1.execute(sql)
        cur_fetchall = self.cur1.fetchall()
        for index, i in enumerate(cur_fetchall):
            abandon_blacklistPerID.append(cur_fetchall[index][0])
        resID_tuple = tuple(abandon_blacklistPerID)
        if len(resID_tuple) == 1:
            sql = 'SELECT ResID from perResume where PerID = %s' % str(resID_tuple[0])
        else:
            sql = 'SELECT ResID from perResume where PerID in %s' % str(resID_tuple)
        self.cur1.execute(sql)
        cur_fetchall = self.cur1.fetchall()
        abandon_black_resID = []
        for index, i in enumerate(cur_fetchall):
            abandon_black_resID.append(cur_fetchall[index][0])
        # self.conn.close()
        print('黑名单表查询成功')
        return abandon_black_resID

    def es_search_present(self, info):
        comID = info['comID']
        keyword = info["keyword"]
        com_name = info["comNameKeyword"]
        job_name = info["jobNameKeyword"]
        school_name = info["schoolNameKeyword"]
        active_day = info['activeDay']
        gender = info["gender"]
        home_area = info["residence"]
        minEdu = info['minEdu']
        maxEdu = info['maxEdu']
        minAge = info['minAge']  # str
        maxAge = info['maxAge']  # str
        wish_salary = info['exceptedSalary']
        wish_salary_label = info['exceptedSalaryLabel']
        minWorkYear = info['minWorkYear']
        maxWorkYear = info['maxWorkYear']
        wish_Job = info['exceptedJob']
        wish_Area = info['exceptedArea']
        deliver_flag = info['deliverFilter']
        download_flag = info['downloadFilter']
        abandon_deliverResid = self.filter_deliver_list(comID, deliver_flag)
        ababdon_downloadResid = self.filter_download_list(comID, download_flag)
        abandon_deliverResid += ababdon_downloadResid
        abandon_resid = list(set(abandon_deliverResid))
        abandon_black_resid = self.filter_blackList(comID)
        abandon_resid += abandon_black_resid
        abandon_resid_new = list(set(abandon_resid))
        body = {
            "size": int(info['pageSize']),
            "from": int(info['pageSize']) * (int(info["pageIndex"]) - 1),
            "query": {
                "bool": {
                    "must": [{"match": {"SetPull": 1}}, {"match": {"IsResumeDone": 1}}],  # TODO 也能查到大量结果，待解决
                    "must_not": [{"terms": {"ResID": abandon_resid_new}}]
                }
            }, "sort": [{"_score": {"order": "desc"}}, {"LoginTime": {"order": "desc"}}],
            "collapse": {"field": "ResID"},
            "aggs": {"total": {"cardinality": {"field": "ResID"}}}
        }
        if keyword != "":
            key = {"multi_match": {"query": keyword,
                                   "fields": ["SchoolName", "ComName", "MajorName", "DeptName", "JobName", "WorkStory", "ExpItem"],
                                   "tie_breaker": 0.3}}
            body.get("query").get('bool').get("must").append(key)
        if com_name != "":
            body.get("query").get('bool').get("must").append({"match": {"ComName": com_name}})
        if job_name != "":
            body.get("query").get('bool').get("must").append({"match": {"JobName": job_name}})
        if school_name != "":
            body.get("query").get('bool').get("must").append({"match": {"SchoolName": school_name}})
        if active_day != "":
            current_time = datetime.datetime.now()  # <class 'datetime.datetime'>
            date = (current_time + datetime.timedelta(days=-int(active_day))).strftime("%Y-%m-%dT%H:%M:%S")  # str
            current_time = current_time.strftime('%Y-%m-%dT%H:%M:%S')  # 格式化 str
            body.get("query").get('bool').get("must").append(
                    {"range": {"LoginTime": {"gte": date, "lte": current_time}}})
        if gender != "":
            body.get("query").get('bool').get("must").append({"match": {"Sex": gender}})
        # 学历规则
        if minEdu == '' and maxEdu == '':
            print('Both minEdu and maxEdu are NULL!')
        else:
            degree_range = mp.edu_change(minEdu, maxEdu)
            body.get("query").get('bool').get("must").append(degree_range)
        # 年龄规则
        if minAge == '' and maxAge == '':
            print('Both minAge and maxAge are NULL!')
        else:
            age_range = mp.age_change(minAge, maxAge)
            body.get("query").get('bool').get("must").append(age_range)
        # 工作年限
        if minWorkYear == '' and maxWorkYear == '':
            print('Both minWorkYear and maxWorkYear are NULL!')
        else:
            work_years_range = mp.works_years(minWorkYear, maxWorkYear)
            body.get("query").get('bool').get("must").append(work_years_range)
        # 薪资规则
        wish_salary_body = mp.salary_change(wish_salary)
        if wish_salary_body:
            body.get("query").get('bool').get("must").append(wish_salary_body)
        # 期待职位
        if wish_Job != "":
            body.get("query").get('bool').get("must").append({"match": {"WishJob": wish_Job}})
        # 期待地区
        if wish_Area != "":
            body.get("query").get('bool').get("must").append({"match": {"WishArea": wish_Area}})
        # 地区涵盖(未测试)
        if home_area != "":
            try:
                home_area = mp.areaExpansion(home_area)
                body.get('query').get('bool').get("must").append({"terms": {'HomeArea': home_area}})
            except:
                body.get('query').get('bool').get("must").append({"match": {'HomeArea': home_area}})
        # es—search
        present_resid = []
        try:
            query = self.es.search(index="res_test", doc_type='doc', body=body)
            if int(query["aggregations"]["total"]['value']) == 0:
                print('输入组合条件未得到结果！')
                return present_resid, 0
        except Exception as e:
            raise e
        else:
            total = int(query["aggregations"]["total"]['value'])
            hits_list = query["hits"]["hits"]  # 查询返回第一页的结果数据
        for dic in hits_list:
            present_resid.append(int(dic['_source'].get("ResID")))
        return present_resid, total


Re = ResumeDao()

'''
if __name__ == '__main__':
    info = {
        "comID": "6864",
        "keyword": "软件昆山去清华",
        "comNameKeyword": "",
        "jobNameKeyword": "",
        "schoolNameKeyword": "",
        "activeDay": "",
        "minEdu": "",
        "maxEdu": "",
        "minAge": "",
        "maxAge": "",
        "gender": "",
        "minWorkYear": "",
        "maxWorkYear": "",
        "residence": "",
        "exceptedJob": "",
        "exceptedArea": "",
        "exceptedSalary": "",
        "exceptedSalaryLabel": "",
        "deliverFilter": "",
        "downloadFilter": "",
        "pageIndex": "1",
        "pageSize": "10"
}

    present_resid, total = Re.es_search_present(info)
    print("resid:", present_resid)
    print('total:', total)
'''
