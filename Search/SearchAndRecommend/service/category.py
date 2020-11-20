from SearchAndRecommend.service.HashTableLoad import IndexView
from SearchAndRecommend.static.class_hash import big_class, small_class1



def Classify(data):
    num1 = data['JobType']
    if num1 != '' and int(num1) in big_class.values():
        num1 = int(num1)
        # 取出大类中的所有小类 + 小类total
        for value in big_class.values():
            if num1 == value:
                for key1 in small_class1.keys():
                    if value == key1:
                        dict1 = small_class1[key1]
                        jobTypeList1 = []
                        for key, val in dict1.items():
                            dict33 = {}
                            dict33['jobType'] = str(int(val))
                            dict33['jobTypeLabel'] = key
                            dict33['jobNum'] = str(IndexView.get_pos_count(val))
                            jobTypeList1.append(dict33)
                        return jobTypeList1
                        # print("list1:", jobTypeList1)
                        # if "total" in dict1.keys():
                        #     dict1["total"] = len(dict1) - 1
                        # #     dict1["total"].append(len(dict1))
                        # else:
                        #     dict1["total"] = len(dict1)
                        # result = json.dumps(dict1, ensure_ascii=False, cls=MyJSONEncoder)
                        # print(type(result))  #str

    # return result
    elif num1 == '':
        # num1为空，默认为不限，返回所有小类列表
        jobTypeList2 = []
        for key, val in big_class.items():
            dict22 = {}
            dict22['jobType'] = str(val)
            dict22['jobTypeLabel'] = key
            dict22['jobNum'] = str(len(small_class1[val]))
            jobTypeList2.append(dict22)
        # print('list2', jobTypeList2)
        return jobTypeList2
    else:
        num1 = int(num1)
        jobTypeList3 = []
        dict44 = {}
        dict44['jobType'] = str(num1)
        for key in small_class1.keys():
            for key1, value1 in small_class1[key].items():
                if int(value1) == num1:
                    dict44['jobTypeLabel'] = key1
        dict44['jobNum'] = str(IndexView.get_pos_count(num1))
        jobTypeList3.append(dict44)
        return jobTypeList3
        # print("list3", jobTypeList3)

    #     # TODO 逻辑判断num2
    #     total_count = IndexView.get_pos_count(num1)
    #     result = GetInfo(result)
    #     result = json.loads(result)
    #     print(type(result))
    #     # result = json.loads(result)
    #     pos_list = statisticalQuantity(result)
    #     # pager = Paginator(1, total_count, per_page=3)
    #     # 分页返回查询到的小类中的职位
    #     # pos_list = IndexView.get_pos(num1)
    #     # result = pos_list[pager.start:pager.end]
    #     pos_list = json.dumps(pos_list)
    #     return pos_list
