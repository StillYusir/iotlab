import sys
sys.path.append('/home/iotlab/Search/')
from elasticsearch import Elasticsearch
from SearchAndRecommend.common.SearchEntiy import Search_preprocess
from SearchAndRecommend.service.convertMessage import deal_category,keyword_sort
from SearchAndRecommend.service.Paginate import Paginator
from datetime import datetime
from SearchAndRecommend.utils.date_match import validate_and_match_datetime

b = Search_preprocess()
es=Elasticsearch([{'host': '127.0.0.1', 'port':8769 }])

# 功能
# 1.分页
# 2.输出为前端标准数据格式

class PP:
    def __init__(self):
        self.joblist = {
            "jobID": "string",
            "comID": "string",
            "comName": "string",
            "comTradeLabel": "string",
            "comScaleLabel": "string",
            "jobName": "string",
            "jobAreaLabel": "string",
            "workExpLabel": "string",
            "eduLabel": "string",
            "minSalary": "string",
            "maxSalary": "string",
            "jobIntro": "string",
            "updateDateTime": "string",
            "isTopJob": "string"
        }
        self.comlist = {"word": "string"}
        self.analyzelist = {"word": "string"}
        self.temp_pos = {
            "data": {
                "jobList": [{
                    "jobID": "string",
                    "comID": "string",
                    "comName": "string",
                    "comTradeLabel": "string",
                    "comScaleLabel": "string",
                    "jobName": "string",
                    "jobAreaLabel": "string",
                    "workExpLabel": "string",
                    "eduLabel": "string",
                    "minSalary": "string",
                    "maxSalary": "string",
                    "jobIntro": "string",
                    "updateDateTime": "string",
                    "isTopJob": "string"

                }
                ],
                "jobTotal": "string",
                "analyzeList":[{"word":"string"}]
            }
        }
        self.temp_com = {
            "data": {"list":
                [
                    {
                        "word": "string"
                    }
                ]
            }}
        self.error_com = {
            "errorCode": "None",
            "errorInfo": "None"
        }

    def post_process_pos(self, search_result, info):
        if search_result['hits']['hits'] == []:
            return self.error_com
        # if info['keyword'] == "" and info['JobArea'] == "" and info["salary"] == "" and info["salaryLabel"] == "" and \
        #         info["JobWorkYears"] == "" \
        #         and info["JobDegree"] == "" and info["JobProperty"] == "" and info["ComEmployee"] == "" and info[
        #     "perID"] == "":
        #     jobtypelist = Classify(info)
        # # 统计各小类数量
        # else:
        #     jobtypelist = statisticalQuantity(search_result)
        jobtypelist = deal_category(search_result, info)
        self.temp_pos.get('data')['jobTypeList'] = jobtypelist
        self.temp_pos.get('data')['jobTotal'] = search_result['hits']['total']
        for index, JSON in enumerate(search_result['hits']['hits']):
            self.temp_pos.get('data')['jobList'][index]['jobID'] = JSON["_source"]['JobID']
            self.temp_pos.get('data')['jobList'][index]['comID'] = JSON["_source"]['ComID']
            self.temp_pos.get('data')['jobList'][index]['comName'] = JSON["_source"]['ComName']
            self.temp_pos.get('data')['jobList'][index]['comTradeLabel'] = JSON["_source"]['ComTradeName']
            self.temp_pos.get('data')['jobList'][index]['comScaleLabel'] = JSON["_source"]['ComScaleName']
            self.temp_pos.get('data')['jobList'][index]['jobName'] = JSON["_source"]['JobName']
            self.temp_pos.get('data')['jobList'][index]['jobAreaLabel'] = JSON["_source"]['JobAreaName']
            self.temp_pos.get('data')['jobList'][index]['workExpLabel'] = JSON["_source"]['JobWorkYearsName']
            self.temp_pos.get('data')['jobList'][index]['eduLabel'] = JSON["_source"]['JobDegreeName']
            self.temp_pos.get('data')['jobList'][index]['minSalary'] = JSON["_source"]['JobPayMin']
            self.temp_pos.get('data')['jobList'][index]['maxSalary'] = JSON["_source"]['JobPayMax']
            self.temp_pos.get('data')['jobList'][index]['jobIntro'] = JSON["_source"]['JobDesc']
            self.temp_pos.get('data')['jobList'][index]['updateDateTime'] = JSON["_source"]['OrderTime']
            #推荐时间大于现在时间，则为推荐职位,大于现在返回1，否则返回0
            if JSON["_source"]['JobTopEndDate'] is None:
                self.temp_pos.get('data')['jobList'][index]['isTopJob'] = 0
            #判断elif
            else:
                # "JobTopEndDate": "2019-02-26T00:00:00"
                text = JSON['_source']['JobTopEndDate']
                top_time = validate_and_match_datetime(str(text))
                top_time = datetime.strptime(top_time, "%Y-%m-%d %H:%M:%S")
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                current_time = datetime.strptime(current_time, "%Y-%m-%d %H:%M:%S")
                if current_time >= top_time:
                    self.temp_pos.get('data')['jobList'][index]['isTopJob'] = 0
                else:
                    self.temp_pos.get('data')['jobList'][index]['isTopJob'] = 1
            if index != (len(search_result['hits']['hits']) - 1):
                self.temp_pos.get('data')['jobList'].append({
            "jobID": "string",
            "comID": "string",
            "comName": "string",
            "comTradeLabel": "string",
            "comScaleLabel": "string",
            "jobName": "string",
            "jobAreaLabel": "string",
            "workExpLabel": "string",
            "eduLabel": "string",
            "minSalary": "string",
            "maxSalary": "string",
            "jobIntro": "string",
            "updateDateTime": "string",
            "isTopJob": "string"
        })
        # 返回jobname对应的分词情况给前端高亮
        if info['keyword'] == "":
            self.temp_pos.get('data')["analyzeList"].pop(0)
        else:
            analyze = {
                "analyzer": "ik_smart",
                "text": info['keyword']
            }
            Analyze = es.indices.analyze(index='keyword', body=analyze)
            lens = len(Analyze.get('tokens'))-1
            for index,j in enumerate(Analyze.get('tokens')):
                self.temp_pos.get('data')["analyzeList"][index]['word'] = j.get('token')
                if index < lens:
                    self.temp_pos.get('data')['analyzeList'].append({"word": "string"})
        return self.temp_pos
        return self.temp_pos

    def post_process_com(self, com_result):
        if com_result['suggest']['my-suggest'][0]['options'] == []:
            return self.error_com
        else:
            com_result = keyword_sort(com_result)
            for index, JSON in enumerate(com_result):
                self.temp_com.get('data')['list'][index]['word'] = JSON["text"]
                if index != (len(com_result) - 1):
                    self.temp_com.get('data')['list'].append({"word": "string"})
        return self.temp_com

if __name__ == '__main__':
    pass
