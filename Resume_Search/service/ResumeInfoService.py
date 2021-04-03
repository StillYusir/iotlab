from dao.resume_dao import Re


class ResumeInfoService:
    # 最终展示
    def present_process(self, info):
        basicInfo = {
            "id": "",
            "realName": "",
            "gender": "",
            "genderLabel": "",
            "birthday": "",
            "residence": "",
            "residenceLabel": "",
            "isHasWorkExp": "",
            "beginWorkDate": "",
            "applyState": "",
            "applyStateLabel": "",
            "edu": "",
            "eduLabel": "",
            "curSalary": "",
            "curSalaryLabel": "",
            "marriage": "",
            "marriageLabel": "",
            "nation": "",
            "nationLabel": "",
            "nativePlace": "",
            "nativePlaceLabel": "",
            "portrait": "",
            "lastLoginDateTime": ""
        }
        jobIntension = {
            "exceptedJob": "",
            "exceptedJobLabel": "",
            "exceptedArea": "",
            "exceptedAreaLabel": "",
            "exceptedMinSalary": "",
            "exceptedMaxSalary": ""
        }

        eduExpList = []
        workExpList = []

        resumeList = [
            {
                "id": "",
                "resumeName": "",
                "projectExp": "",
                "skill": "",
                "appendInfo": "",
                "isDownloaded": "",
                "updateDate": "",
                "basicInfo": basicInfo,
                "jobIntension": jobIntension,
                "eduExpList": eduExpList,
                "workExpList": workExpList
            }
        ]
        Analyze_List = {
            'analyzeList': [
                {
                    "word": ""
                }
            ],
            'comNameAnalyzeList': [
                {
                    "word": ""
                }
            ],
            'jobNameAnalyzeList': [
                {
                    "word": ""
                }
            ],
            'schoolNameAnalyzeList': [
                {
                    "word": ""
                }
            ]
        }
        response = {
            "data": {
                "resumeList": resumeList,
                "resumeTotal": "",
                "analyzeList": Analyze_List.get('analyzeList'),
                "comNameAnalyzeList": Analyze_List.get('comNameAnalyzeList'),
                "jobNameAnalyzeList": Analyze_List.get('jobNameAnalyzeList'),
                "schoolNameAnalyzeList": Analyze_List.get('schoolNameAnalyzeList')
            }
        }
        error_res = {
            "errorCode": "None",
            "errorInfo": "None"
        }

        present_resid, total = Re.es_search_present(info)
        if total == 0:
            return error_res

        # 分词返回
        analyze1 = {
            "analyzer": "ik_smart",
            "text": info['keyword']
        }
        analyze2 = {
            "analyzer": "ik_smart",
            "text": info['comNameKeyword']
        }
        analyze3 = {
            "analyzer": "ik_smart",
            "text": info['jobNameKeyword']
        }
        analyze4 = {
            "analyzer": "ik_smart",
            "text": info['schoolNameKeyword']
        }
        if info['keyword'] == "":
            Analyze_List.get('analyzeList').pop(0)
        else:
            Analyze1 = Re.es.indices.analyze(index='res_test', body=analyze1)
            lens = len(Analyze1.get('tokens')) - 1
            for index, j in enumerate(Analyze1.get('tokens')):
                Analyze_List.get('analyzeList')[index]['word'] = j.get('token')
                if index < lens:
                    Analyze_List.get('analyzeList').append({"word": "string"})
        if info['comNameKeyword'] == "":
            Analyze_List.get('comNameAnalyzeList').pop(0)
        else:
            Analyze2 = Re.es.indices.analyze(index='res_test', body=analyze2)
            lens = len(Analyze2.get('tokens')) - 1
            for index, j in enumerate(Analyze2.get('tokens')):
                Analyze_List.get('comNameAnalyzeList')[index]['word'] = j.get('token')
                if index < lens:
                    Analyze_List.get('comNameAnalyzeList').append({"word": "string"})
        if info['jobNameKeyword'] == "":
            Analyze_List.get('jobNameAnalyzeList').pop(0)
        else:
            Analyze3 = Re.es.indices.analyze(index='res_test', body=analyze3)
            lens = len(Analyze3.get('tokens')) - 1
            for index, j in enumerate(Analyze3.get('tokens')):
                Analyze_List.get('jobNameAnalyzeList')[index]['word'] = j.get('token')
                if index < lens:
                    Analyze_List.get('jobNameAnalyzeList').append({"word": "string"})
        if info['schoolNameKeyword'] == "":
            Analyze_List.get('schoolNameAnalyzeList').pop(0)
        else:
            Analyze4 = Re.es.indices.analyze(index='res_test', body=analyze4)
            lens = len(Analyze4.get('tokens')) - 1
            for index, j in enumerate(Analyze4.get('tokens')):
                Analyze_List.get('schoolNameAnalyzeList')[index]['word'] = j.get('token')
                if index < lens:
                    Analyze_List.get('schoolNameAnalyzeList').append({"word": "string"})
        # 将10个resid分为两组，一组是已下载的，一组是为未下载的
        has_download, has_not_download = Re.differ_download_list(present_resid, info['comID'])
        for index, resid in enumerate(present_resid):
            body = {"query": {"match": {"ResID": int(resid)}}}
            try:
                query = Re.es.search(index="res_test", doc_type='doc', body=body)
            except Exception as e:
                raise e
            else:
                hits_list = query["hits"]["hits"]
                # resumeList拼装
                resumeList[index]['id'] = hits_list[0]['_source'].get('ResID')
                resumeList[index]['resumeName'] = hits_list[0]['_source'].get('ResumeName')
                resumeList[index]['projectExp'] = hits_list[0]['_source'].get('ExpItem')
                resumeList[index]['skill'] = hits_list[0]['_source'].get('ExpSkill')
                resumeList[index]['appendInfo'] = hits_list[0]['_source'].get('ExpAddons')
                if info['downloadFilter'] == '1':
                    # 返回'未下载'的简历--对应为0
                    resumeList[index]['isDownloaded'] = '0'
                if info['downloadFilter'] == '0':
                    # 查询abandon_downdList中是否存在该 resid，存在返回1，不存在返回0
                    if resid in has_download:
                        resumeList[index]['isDownloaded'] = '1'
                    if resid in has_not_download:
                        resumeList[index]['isDownloaded'] = '0'
                if hits_list[0]['_source'].get('UpTime') != '':
                    resumeList[index]['updateDate'] = hits_list[0]['_source'].get('UpTime')
                if hits_list[0]['_source'].get('UpTime') == '':
                    resumeList[index]['updateDate'] = hits_list[0]['_source'].get('InTime')
                # basicInfo拼装
                basicInfo['id'] = hits_list[0]['_source'].get('PerID')
                basicInfo['realName'] = hits_list[0]['_source'].get('RealName')
                basicInfo['gender'] = hits_list[0]['_source'].get('Sex')
                basicInfo['genderLabel'] = hits_list[0]['_source'].get('SexName')
                basicInfo['birthday'] = hits_list[0]['_source'].get('BirthDate')
                basicInfo['residence'] = hits_list[0]['_source'].get('WorkArea')
                basicInfo['residenceLabel'] = hits_list[0]['_source'].get('WorkAreaName')
                basicInfo['isHasWorkExp'] = hits_list[0]['_source'].get('IsWorked')
                basicInfo['beginWorkDate'] = hits_list[0]['_source'].get('BeginWorkDate')
                basicInfo['applyState'] = hits_list[0]['_source'].get('WorkState')
                basicInfo['applyStateLabel'] = hits_list[0]['_source'].get('WorkStateName')
                basicInfo['edu'] = hits_list[0]['_source'].get('Degree')
                basicInfo['eduLabel'] = hits_list[0]['_source'].get('DegreeName')
                basicInfo['curSalary'] = hits_list[0]['_source'].get('CurSalary')
                basicInfo['curSalaryLabel'] = hits_list[0]['_source'].get('CurSalaryName')
                basicInfo['marriage'] = hits_list[0]['_source'].get('Marriage')
                basicInfo['marriageLabel'] = hits_list[0]['_source'].get('MarriageName')
                basicInfo['nation'] = hits_list[0]['_source'].get('Nation')
                basicInfo['nationLabel'] = hits_list[0]['_source'].get('NationName')
                basicInfo['nativePlace'] = hits_list[0]['_source'].get('HomeArea')
                basicInfo['nativePlaceLabel'] = hits_list[0]['_source'].get('HomeAreaName')
                basicInfo['portrait'] = hits_list[0]['_source'].get('PhotoURL')
                basicInfo['lastLoginDateTime'] = hits_list[0]['_source'].get('LoginTime')
                # jobintension 拼装
                # TODO 此字典需做映射  举例：1018-1306|1016-1278|   或  1017-1291|1017-1290|1016-1282|1016-1284|
                jobIntension['exceptedJob'] = hits_list[0]['_source'].get('WishJob')
                jobIntension['exceptedJobLabel'] = hits_list[0]['_source'].get('WishJobName')
                jobIntension['exceptedArea'] = hits_list[0]['_source'].get('WishArea')
                jobIntension['exceptedAreaLabel'] = hits_list[0]['_source'].get('WishAreaName')
                jobIntension['exceptedMinSalary'] = hits_list[0]['_source'].get('WishSalaryMin')
                jobIntension['exceptedMaxSalary'] = hits_list[0]['_source'].get('WishSalaryMax')

                edu_id = []
                work_id = []
                for dic in hits_list:
                    # eduExpList 拼装
                    eduID = dic.get('_source').get('Edu_ID')
                    if eduID != '' and eduID not in edu_id:
                        edu_id.append(eduID)
                        eduDict = dict()
                        eduDict['schoolName'] = dic['_source'].get('SchoolName')
                        eduDict['edu'] = dic['_source'].get('Degree')
                        eduDict['eduLabel'] = dic['_source'].get('DegreeName')
                        eduDict['major'] = dic['_source'].get('MajorName')
                        eduDict['beginDate'] = dic['_source'].get('Edu_BeginDate')
                        eduDict['endDate'] = dic['_source'].get('Edu_EndDate')
                        eduDict['intro'] = dic['_source'].get('Story')
                        eduExpList.append(eduDict)
                    # workExpList 拼装
                    workID = dic.get('_source').get("Work_ID")
                    if workID != "" and workID not in work_id:
                        work_id.append(workID)
                        workDict = dict()
                        workDict['comName'] = dic['_source'].get('ComName')
                        workDict['jobName'] = dic['_source'].get('JobName')
                        workDict['beginDate'] = dic['_source'].get('Work_BeginDate')
                        workDict['endDate'] = dic['_source'].get('Work_EndDate')
                        workDict['trade'] = dic['_source'].get('Trade')
                        workDict['tradeLabel'] = dic['_source'].get('TradeName')
                        workDict['jobNature'] = dic['_source'].get('Property')
                        workDict['jobNatureLabel'] = dic['_source'].get('PropertyName')
                        workDict['deptName'] = dic['_source'].get('DeptName')
                        workDict['comScale'] = dic['_source'].get('Employee')
                        workDict['comScaleLabel'] = dic['_source'].get('EmployeeName')
                        workDict['intro'] = dic['_source'].get('Story')
                        workExpList.append(workDict)
                # 复合字典拼装
                resumeList[index]['basicInfo'] = basicInfo
                resumeList[index]['jobIntension'] = jobIntension
                resumeList[index]['eduExpList'] = eduExpList
                resumeList[index]['workExpList'] = workExpList

                if index != (len(present_resid) - 1):
                    basicInfo = {
                        "id": "",
                        "realName": "",
                        "gender": "",
                        "genderLabel": "",
                        "birthday": "",
                        "residence": "",
                        "residenceLabel": "",
                        "isHasWorkExp": "",
                        "beginWorkDate": "",
                        "applyState": "",
                        "applyStateLabel": "",
                        "edu": "",
                        "eduLabel": "",
                        "curSalary": "",
                        "curSalaryLabel": "",
                        "marriage": "",
                        "marriageLabel": "",
                        "nation": "",
                        "nationLabel": "",
                        "nativePlace": "",
                        "nativePlaceLabel": "",
                        "portrait": "",
                        "lastLoginDateTime": ""
                    }
                    jobIntension = {
                        "exceptedJob": "",
                        "exceptedJobLabel": "",
                        "exceptedArea": "",
                        "exceptedAreaLabel": "",
                        "exceptedMinSalary": "",
                        "exceptedMaxSalary": ""
                    }

                    eduExpList = []
                    workExpList = []

                    resumeList.append({
                        "id": "string",
                        "resumeName": "string",
                        "projectExp": "string",
                        "skill": "string",
                        "appendInfo": "string",
                        "isDownloaded": "string",
                        "updateDate": "string",
                        "basicInfo": basicInfo,
                        "jobIntension": jobIntension,
                        "eduExpList": eduExpList,
                        "workExpList": workExpList
                    })
        # response拼装 返回
        response['data']['resumeList'] = resumeList
        response['data']['resumeTotal'] = str(total)
        return response


RIS = ResumeInfoService()
