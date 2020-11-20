
# from SearchAndRecommend.data.PropertiesMapper import temp_pos,temp_com
from SearchAndRecommend.control.SearchEntiy import Search_preprocess
from SearchAndRecommend.service.convertMessage import statisticalQuantity
from SearchAndRecommend.service.Paginate import Paginator
from SearchAndRecommend.service.category import Classify
# import synonyms
b = Search_preprocess()

#功能
#1.分页
#2.输出为前端标准数据格式



class PP:
    def __init__(self):
        self.joblist={
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
        self.comlist={"word": "string"}
        self.temp_pos={
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
    "jobTotal": "string"
  }
}
        self.temp_com={
            "data": {"list":
    [
      {
        "word": "string"
      }
    ]
  }}
        self.error_com={
  "errorCode": "None",
  "errorInfo": "None"
}

    def post_process_pos(self,search_result,info):
        if search_result['hits']['hits']==[]:
            return self.error_com
        if info['keyword']=="" and info['JobArea']==""and info["salary"]==""and info["salaryLabel"]=="" and info["JobWorkYears"]=="" \
            and info["JobDegree"]=="" and info["JobProperty"]=="" and info["ComEmployee"]=="" and info["perID"]=="":
            jobtypelist=Classify(info)
        # 统计各小类数量
        else:
            jobtypelist=statisticalQuantity(search_result)
        self.temp_pos.get('data')['jobTypeList']=jobtypelist
        self.temp_pos.get('data')['jobTotal'] =search_result['hits']['total']
        #处理页数，个数异常
        try:
            int(info["pageIndex"]),int(info["pageSize"])
        except:
            info["pageIndex"],info["pageSize"]=1,20
        pager = Paginator(info["pageIndex"], search_result['hits']['total'], info["pageSize"])
        search_result=search_result['hits']['hits'][pager.start:pager.end]
        for index,JSON  in enumerate(search_result):
            self.temp_pos.get('data')['jobList'][index]['jobID'] = JSON["_source"]['JobID']
            self.temp_pos.get('data')['jobList'][index]['comID'] = JSON["_source"]['ComID']
            self.temp_pos.get('data')['jobList'][index]['comName'] = JSON["_source"]['ComName']
            self.temp_pos.get('data')['jobList'][index]['comTradeLabel'] = JSON["_source"]['JobPropertyName']
            self.temp_pos.get('data')['jobList'][index]['comScaleLabel'] = JSON["_source"]['ComEmployeeName']
            self.temp_pos.get('data')['jobList'][index]['jobName'] = JSON["_source"]['JobName']
            self.temp_pos.get('data')['jobList'][index]['jobAreaLabel'] = JSON["_source"]['JobAreaName']
            self.temp_pos.get('data')['jobList'][index]['workExpLabel'] = b.Map_year2num(int(JSON["_source"]['JobWorkYears']))
            self.temp_pos.get('data')['jobList'][index]['eduLabel'] = JSON["_source"]['JobDegreeName']
            self.temp_pos.get('data')['jobList'][index]['minSalary'] = JSON["_source"]['JobPayMin']
            self.temp_pos.get('data')['jobList'][index]['maxSalary'] = JSON["_source"]['JobPayMax']
            self.temp_pos.get('data')['jobList'][index]['jobIntro'] = JSON["_source"]['JobDesc']
            self.temp_pos.get('data')['jobList'][index]['updateDateTime'] = JSON["_source"]['UpTime']
            self.temp_pos.get('data')['jobList'][index]['isTopJob'] = JSON["_source"]['IsDel']
            if index != (len(search_result) - 1):
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
        return self.temp_pos

    def post_process_com(self,com_result):
        if com_result['suggest']['my-suggest'][0]['options']==[]:
            return self.error_com
        else:
            com_result=com_result['suggest']['my-suggest'][0]['options']
            for index,JSON in enumerate(com_result):
                self.temp_com.get('data')['list'][index]['word']=JSON["text"]
                if index!=(len(com_result)-1):
                    self.temp_com.get('data')['list'].append({"word": "string"})
        return self.temp_com


if __name__ == '__main__':
    b = Search_preprocess()
    a = [
    {
        "JobID": "241728",
        "ComID": "8825",
        "ComName": "江苏冠道信息科技有限公司",
        "JobName": "行政主管",
        "JobWorkYears": "3508",
        "JobSex": "3201",
        "JobSexName": "不限",
        "JobType": "211120",
        "JobTypeName": "其他职位",
        "JobProperty": "1204",
        "JobPropertyName": "民营",
        "ComEmployee": "1303",
        "ComEmployeeName": "100-500人",
        "JobDegree": "3402",
        "JobDegreeName": "本科",
        "JobArea": "32058301",
        "JobAreaName": "苏州-昆山",
        "JobPayMin": "0",
        "JobPayMax": "8",
        "JobAgeMin": "20",
        "JobAgeMax": "50",
        "JobMans": "1",
        "JobBeginDate": "2020-1-1 ",
        "JobEndDate": "2020-12-10 ",
        "JobTopEndDate": "2021-1-6 ",
        "InTime": "2020-4-23 9:23:21",
        "UpTime": "2020-4-23 8:42:59",
        "JobAddress": "锦溪镇锦东路455号",
        "CountView": "1",
        "IsDel": "0",
        "JobLight": "发展空间大|带薪年假|定期体检|岗位晋升|包吃包住"
    },
    {
        "JobID": "184867",
        "ComID": "9067",
        "ComName": "江苏冠道信息科技有限公司",
        "JobName": "激光下料员",
        "JobWorkYears": "3508",
        "JobSex": "3201",
        "JobSexName": "不限",
        "JobType": "211120",
        "JobTypeName": "项目经理/主管",
        "JobProperty": "1202",
        "JobPropertyName": "民营",
        "ComEmployee": "1303",
        "ComEmployeeName": "100-500人",
        "JobDegree": "3404",
        "JobDegreeName": "不限",
        "JobArea": "32058318",
        "JobAreaName": "昆山-千灯",
        "JobPayMin": "6",
        "JobPayMax": "6",
        "JobAgeMin": "20",
        "JobAgeMax": "50",
        "JobMans": "4",
        "JobBeginDate": "2020-2-21 ",
        "JobEndDate": "2020-12-31 ",
        "JobTopEndDate": "NULL",
        "InTime": "2020-4-23 8:50:17",
        "UpTime": "2020-4-23 9:1:46",
        "JobAddress": "北门路3199号申凌科技园内",
        "CountView": "0",
        "IsDel": "0",
        "JobLight": "发展空间大|带薪年假|定期体检|五险一金"
    },
    {
        "JobID": "265942",
        "ComID": "54952",
        "ComName": "江苏冠道信息科技有限公司",
        "JobName": "行政主管",
        "JobWorkYears": "3508",
        "JobSex": "3201",
        "JobSexName": "不限",
        "JobType": "211700",
        "JobTypeName": "钳工",
        "JobProperty": "1202",
        "JobPropertyName": "外资(非欧美)",
        "ComEmployee": "1303",
        "ComEmployeeName": "1000-10000人",
        "JobDegree": "3405",
        "JobDegreeName": "初中及以下",
        "JobArea": "32058301",
        "JobAreaName": "昆山-开发区",
        "JobPayMin": "6",
        "JobPayMax": "5",
        "JobAgeMin": "48",
        "JobAgeMax": "50",
        "JobMans": "1",
        "JobBeginDate": "2020-1-1 ",
        "JobEndDate": "2020-12-10 ",
        "JobTopEndDate": "NULL",
        "InTime": "2020-4-23 9:23:21",
        "UpTime": "2020-4-23 8:42:59",
        "JobAddress": "昆山开发区澄湖路248号",
        "CountView": "2",
        "IsDel": "0",
        "JobLight": "发展空间大|带薪年假|定期体检|五险一金"
    },
    {
        "JobID": "683140",
        "ComID": "54952",
        "ComName": "江苏冠道信息科技有限公司",
        "JobName": "助理",
        "JobWorkYears": "3508",
        "JobSex": "0",
        "JobSexName": "不限",
        "JobType": "214706",
        "JobTypeName": "销售",
        "JobProperty": "1202",
        "JobPropertyName": "外资(非欧美)",
        "ComEmployee": "1303",
        "ComEmployeeName": "1000-10000人",
        "JobDegree": "3404",
        "JobDegreeName": "大专",
        "JobArea": "32058318",
        "JobAreaName": "昆山-高新区",
        "JobPayMin": "8",
        "JobPayMax": "5",
        "JobAgeMin": "47",
        "JobAgeMax": "50",
        "JobMans": "3",
        "JobBeginDate": "2020-1-17 ",
        "JobEndDate": "2020-12-10 ",
        "JobTopEndDate": "NULL",
        "InTime": "2020-4-23 8:16:28",
        "UpTime": "2020-4-21 13:49:26",
        "JobAddress": "昆山花桥顺扬工业区横塘路102号",
        "CountView": "0",
        "IsDel": "0",
        "JobLight": "发展空间大|技能培训|岗位晋升|五险一金|包吃包住|全勤奖"
    },
    {
        "JobID": "782702",
        "ComID": "54952",
        "ComName": "江苏冠道信息科技有限公司",
        "JobName": "机械设计",
        "JobWorkYears": "3508",
        "JobSex": "0",
        "JobSexName": "不限",
        "JobType": "219900",
        "JobTypeName": "其他职位",
        "JobProperty": "1204",
        "JobPropertyName": "外资(非欧美)",
        "ComEmployee": "1305",
        "ComEmployeeName": "100-500人",
        "JobDegree": "3404",
        "JobDegreeName": "中专/中技",
        "JobArea": "32058316",
        "JobAreaName": "昆山-高新区",
        "JobPayMin": "6",
        "JobPayMax": "4",
        "JobAgeMin": "21",
        "JobAgeMax": "50",
        "JobMans": "5",
        "JobBeginDate": "2020-2-25 ",
        "JobEndDate": "2020-12-10 ",
        "JobTopEndDate": "NULL",
        "InTime": "2020-4-23 9:12:40",
        "UpTime": "2020-4-23 9:1:46",
        "JobAddress": "青阳支路33号",
        "CountView": "0",
        "IsDel": "0",
        "JobLight": "发展空间大|带薪年假|五险一金"
    },
    {
        "JobID": "675306",
        "ComID": "54952",
        "ComName": "江苏冠道信息科技有限公司",
        "JobName": "机械设计",
        "JobWorkYears": "3508",
        "JobSex": "0",
        "JobSexName": "不限",
        "JobType": "219900",
        "JobTypeName": "其他职位",
        "JobProperty": "1204",
        "JobPropertyName": "民营",
        "ComEmployee": "1303",
        "ComEmployeeName": "100-500人",
        "JobDegree": "3402",
        "JobDegreeName": "不限",
        "JobArea": "32058318",
        "JobAreaName": "昆山-开发区",
        "JobPayMin": "10",
        "JobPayMax": "8",
        "JobAgeMin": "20",
        "JobAgeMax": "50",
        "JobMans": "2",
        "JobBeginDate": "2020-2-5 ",
        "JobEndDate": "2020-12-31 ",
        "JobTopEndDate": "NULL",
        "InTime": "2020-4-17 13:32:42",
        "UpTime": "2020-3-25 13:51:14",
        "JobAddress": "昆山花桥顺扬工业区横塘路102号",
        "CountView": "0",
        "IsDel": "0",
        "JobLight": "发展空间大|绩效奖金|带薪年假|五险一金|包吃包住"
    },
    {
        "JobID": "871286",
        "ComID": "8825",
        "ComName": "江苏冠道信息科技有限公司",
        "JobName": "安全管理经理",
        "JobWorkYears": "3508",
        "JobSex": "3201",
        "JobSexName": "男",
        "JobType": "219900",
        "JobTypeName": "客服",
        "JobProperty": "1202",
        "JobPropertyName": "民营",
        "ComEmployee": "1303",
        "ComEmployeeName": "100-500人",
        "JobDegree": "3404",
        "JobDegreeName": "不限",
        "JobArea": "32058312",
        "JobAreaName": "昆山-开发区",
        "JobPayMin": "6",
        "JobPayMax": "0",
        "JobAgeMin": "20",
        "JobAgeMax": "50",
        "JobMans": "1",
        "JobBeginDate": "2020-2-7 ",
        "JobEndDate": "2020-12-10 ",
        "JobTopEndDate": "NULL",
        "InTime": "2020-3-25 13:50:11",
        "UpTime": "2020-4-23 9:46:43",
        "JobAddress": "吴江经济开发区",
        "CountView": "0",
        "IsDel": "0",
        "JobLight": "发展空间大|带薪年假|技能培训|岗位晋升|五险一金"
    },
    {
        "JobID": "312588",
        "ComID": "8825",
        "ComName": "江苏冠道信息科技有限公司",
        "JobName": "行政兼出纳",
        "JobWorkYears": "3508",
        "JobSex": "0",
        "JobSexName": "女",
        "JobType": "211400",
        "JobTypeName": "其他职位",
        "JobProperty": "1202",
        "JobPropertyName": "外资(非欧美)",
        "ComEmployee": "1305",
        "ComEmployeeName": "1000-10000人",
        "JobDegree": "3405",
        "JobDegreeName": "大专",
        "JobArea": "32058301",
        "JobAreaName": "昆山-开发区",
        "JobPayMin": "6",
        "JobPayMax": "5",
        "JobAgeMin": "20",
        "JobAgeMax": "50",
        "JobMans": "0",
        "JobBeginDate": "2020-2-28 ",
        "JobEndDate": "2020-12-10 ",
        "JobTopEndDate": "NULL",
        "InTime": "2020-4-23 9:23:21",
        "UpTime": "2020-4-22 20:33:34",
        "JobAddress": "昆山市锦溪镇锦东路455号",
        "CountView": "1",
        "IsDel": "0",
        "JobLight": "发展空间大|绩效奖金|带薪年假|五险一金"
    },
    {
        "JobID": "834549",
        "ComID": "1832",
        "ComName": "江苏冠道信息科技有限公司",
        "JobName": "CNC操机",
        "JobWorkYears": "3508",
        "JobSex": "0",
        "JobSexName": "女",
        "JobType": "213153",
        "JobTypeName": "模具工",
        "JobProperty": "1202",
        "JobPropertyName": "外资(非欧美)",
        "ComEmployee": "1303",
        "ComEmployeeName": "100-500人",
        "JobDegree": "3405",
        "JobDegreeName": "中专/中技",
        "JobArea": "32058301",
        "JobAreaName": "昆山-千灯",
        "JobPayMin": "0",
        "JobPayMax": "0",
        "JobAgeMin": "20",
        "JobAgeMax": "40",
        "JobMans": "2",
        "JobBeginDate": "2020-2-6 ",
        "JobEndDate": "2020-12-10 ",
        "JobTopEndDate": "NULL",
        "InTime": "2020-4-23 8:50:17",
        "UpTime": "2020-4-23 9:20:20",
        "JobAddress": "吴淞江南路158号靠近昆嘉路",
        "CountView": "0",
        "IsDel": "0",
        "JobLight": "发展空间大|绩效奖金|交通补助|技能培训|岗位晋升|工作轻松"
    },
    {
        "JobID": "945021",
        "ComID": "8825",
        "ComName": "江苏冠道信息科技有限公司",
        "JobName": "EMCRF测试工程师",
        "JobWorkYears": "3508",
        "JobSex": "0",
        "JobSexName": "不限",
        "JobType": "213123",
        "JobTypeName": "钳工",
        "JobProperty": "1202",
        "JobPropertyName": "外资(非欧美)",
        "ComEmployee": "1305",
        "ComEmployeeName": "1000-10000人",
        "JobDegree": "3403",
        "JobDegreeName": "不限",
        "JobArea": "32058301",
        "JobAreaName": "昆山-高新区",
        "JobPayMin": "6",
        "JobPayMax": "8",
        "JobAgeMin": "26",
        "JobAgeMax": "50",
        "JobMans": "2",
        "JobBeginDate": "2020-2-29 ",
        "JobEndDate": "2020-12-10 ",
        "JobTopEndDate": "2021-1-5 ",
        "InTime": "2020-4-23 8:50:17",
        "UpTime": "2020-4-23 9:1:46",
        "JobAddress": "昆嘉路337号",
        "CountView": "1",
        "IsDel": "0",
        "JobLight": "发展空间大|五险一金|团队聚餐"
    }]




    # for index,JSON  in enumerate(a):
    #     temp_pos.get('data')['jobList'][index]['jobID'] = JSON['JobID']
    #     temp_pos.get('data')['jobList'][index]['comID'] = JSON['ComID']
    #     temp_pos.get('data')['jobList'][index]['comName'] = JSON['ComName']
    #     temp_pos.get('data')['jobList'][index]['comTradeLabel'] = JSON['JobPropertyName']
    #     temp_pos.get('data')['jobList'][index]['comScaleLabel'] = JSON['ComEmployeeName']
    #     temp_pos.get('data')['jobList'][index]['jobName'] = JSON['JobName']
    #     temp_pos.get('data')['jobList'][index]['jobAreaLabel'] = JSON['JobAreaName']
    #     temp_pos.get('data')['jobList'][index]['workExpLabel'] = b.Map_year2num(int(JSON['JobWorkYears']))
    #     temp_pos.get('data')['jobList'][index]['eduLabel'] = JSON['JobDegreeName']
    #     temp_pos.get('data')['jobList'][index]['minSalary'] = JSON['JobPayMin']
    #     temp_pos.get('data')['jobList'][index]['maxSalary'] = JSON['JobPayMax']
    #     temp_pos.get('data')['jobList'][index]['jobIntro'] = JSON['JobLight']
    #     temp_pos.get('data')['jobList'][index]['updateDateTime'] = JSON['UpTime']
    #     temp_pos.get('data')['jobList'][index]['isTopJob'] = JSON['ComID']
    #     # print(JSON)
    #     # print(index)
    # print(temp_pos)
