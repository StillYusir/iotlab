import json as js
from SearchAndRecommend.data.PropertiesMapper import workYearMapper,PayMax,PayMin

class Search_preprocess:

    # def make_dict(self,json_record):
    #     self.Search_dict=js.loads(json_record)
    #     return self.Search_dict

    # def Map_degree(self,degree):
    #     return {
    #         '初中及以下':degreeMapper[0],
    #         '中专/中技':degreeMapper[1],
    #         '高中':degreeMapper[2],
    #         '大专':degreeMapper[3],
    #         '本科':degreeMapper[4],
    #         '硕士':degreeMapper[5],
    #         '博士及以上':degreeMapper[6]
    #     }.get(degree)
    #TODO 映射待协商
    def Map_salary(self,salary):
        return {
            '2k以下':[PayMax[0],PayMin[0]],
            '2k-3k':[PayMax[1],PayMin[1]],
            '3k-5k':[PayMax[2],PayMin[2]],
            '5k-8k':[PayMax[3],PayMin[3]],
            '8k-12k':[PayMax[4],PayMin[4]],
            '12k-20k':[PayMax[5],PayMin[5]],
            '20k-30k':[PayMax[6],PayMin[6]],
            '30k以上':[999999,PayMin[7]],
            '不限':[999999,0]
        }.get(salary)


    def Map_years(self,WorkYear):

        return {
            '在校生':workYearMapper[0],
            '应届生':workYearMapper[1],
            '1年以内':workYearMapper[2],
            '1-2年':workYearMapper[3],
            '2-3年':workYearMapper[4],
            '3-5年':workYearMapper[5],
            '5-10年':workYearMapper[6],
            '10年以上':workYearMapper[7]

        }.get(WorkYear)












if __name__ == '__main__':
    s = js.loads('{"name":"test", "type":{"name":"seq", "parameter":["1", "2"]}}')
    print(s)
    print(s["name"])
    print(s["type"]["name"])
    print (s["type"]["parameter"][1])
    a=Search_preprocess()
    print(a.Map_years("在校生"))
    print(type(a.Map_years("在校生")))