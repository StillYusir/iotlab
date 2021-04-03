# -*- coding:utf-8 -*-
import sys
sys.path.append('/home/iotlab/Search/')
from SearchAndRecommend.static.area_hash import areaDict
from SearchAndRecommend.service.HashTableLoad import IndexView
from SearchAndRecommend.static.class_hash import small_class1

area = {"昆山市": "32058300"}
zone = {"32058300": {"32058301": "开发区", "32058302": "高新区", "32058303": "花桥开发区", "32058304": "旅游度假区",
                     "32058311": "张浦镇", "32058312": "周市镇", "32058313": "陆家镇", "32058314": "巴城镇",
                     "32058315": "千灯镇", "32058316": "淀山湖镇", "32058317": "周庄镇", "32058318": "锦溪镇"}}


def convertSalary(salary):
    if salary == "不限":
        return '#', '#'
    elif salary == "2k以下":
        return '#', '2'
    elif salary == '2k-3k':
        return '2', '3'
    elif salary == '3k-4k':
        return '3', '4'
    elif salary == '5k-8k':
        return '5', '8'
    elif salary == '8k-12k':
        return '8', '12'
    elif salary == '12k-20k':
        return '12', '20'
    else:
        return '20', '#'


def deal_category(queryResult, info):
    large_buckets = queryResult['aggregations']['group_by_jobtype'].get('buckets')  # 无结果为空list
    if info["keyword"] == '':
        if info["JobType"] == '':
            if info["JobArea"] == '' and info["salary"] == '' and info["ComScale"] == '' and info["ComTrade"] == '' \
                    and info["JobDegree"] == '' and info["JobWorkYears"] == '':
                # jobtype为空，默认为不限，返回包含职位数量最多的前20小类
                # TODO 静态 剔除过期日期
                val_list = IndexView.init_get_pos_count(IndexView)
                for dict1 in val_list:
                    for key in small_class1.keys():
                        for key1, value1 in small_class1[key].items():
                            if int(value1) == int(dict1["jobType"]):
                                dict1['jobTypeLabel'] = key1
                sort_list = sorted(val_list, key=lambda value: int(value.__getitem__('jobNum')), reverse=True)
                return sort_list[:20]
            else:
                jobList = []
                for dic in large_buckets:
                    dict1 = {}
                    dict1["jobType"] = dic.get('key')
                    dict1["jobTypeLabel"] = dic.get('group_by_jobtype_name').get('buckets')[0].get('key')
                    dict1["jobNum"] = dic.get('doc_count')
                    if dict1 not in jobList:
                        jobList.append(dict1)
                sort_list = sorted(jobList, key=lambda value: int(value.__getitem__('jobNum')), reverse=True)
                return sort_list[:20]
        else:
            # 结果确定，传入类别，返回当前小类
            dict2 = {}
            jobTypeList = []
            dict2["jobType"] = large_buckets[0].get('key')
            dict2['jobTypeLabel'] = large_buckets[0].get('group_by_jobtype_name').get('buckets')[0].get('key')
            dict2['jobNum'] = large_buckets[0].get('doc_count')
            jobTypeList.append(dict2)
            return jobTypeList
    else:
        if info["JobType"] == '':
            # 返回前20
            jobList1 = []
            for dic in large_buckets:
                dict1 = {}
                dict1["jobType"] = dic.get('key')
                dict1["jobTypeLabel"] = dic.get('group_by_jobtype_name').get('buckets')[0].get('key')
                dict1["jobNum"] = dic.get('doc_count')
                if dict1 not in jobList1:
                    jobList1.append(dict1)
            sort_list = sorted(jobList1, key=lambda value: int(value.__getitem__('jobNum')), reverse=True)
            return sort_list[:20]
        else:
            # 类别确定，返回当前小类
            dict2 = {}
            jobTypeList2 = []
            dict2["jobType"] = large_buckets[0].get('key')
            dict2['jobTypeLabel'] = large_buckets[0].get('group_by_jobtype_name').get('buckets')[0].get('key')
            dict2['jobNum'] = large_buckets[0].get('doc_count')
            jobTypeList2.append(dict2)
            return jobTypeList2


def areaExpansion(area):
    return areaDict[area]


def keyword_sort(queryResult):
    res = queryResult['suggest']['my-suggest'][0]['options']
    res = sorted(res, key=lambda x: int(x['_source']['hits'] if x['_source']['IsStop'] == 0 else 0), reverse=True)
    return res[0:10]


def get_number(char):
    count = 0
    for item in char:
        if 0x4E00 <= ord(item) <= 0x9FA5:
            count += 1
    return count


if __name__ == '__main__':
    pass
