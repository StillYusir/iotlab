import json as js
from SearchAndRecommend.data.PropertiesMapper import workYearMapper, PayMax, PayMin, degreeMax, degreeMin


class Search_preprocess:

    def Map_sex(self, sex):
        return {
            '3201': ['3201'],
            '3202': ['3202'],
            '3203': ['3201', '3202']
        }

    # def Map_degree(self,minEdu,maxEdu):
    #     if minEdu == "":
    #         minEdu = 3401
    #
    #     return {
    #         '初中及以下':degreeMapper[0],
    #         '中专/中技':degreeMapper[1],
    #         '高中':degreeMapper[2],
    #         '大专':degreeMapper[3],
    #         '本科':degreeMapper[4],
    #         '硕士':degreeMapper[5],
    #         '博士及以上':degreeMapper[6]
    #     }.get(degree)

    def Map_salary(self, salary):
        return {
            '2k以下': [PayMax[0], PayMin[0]],
            '2-3k': [PayMax[1], PayMin[1]],
            '3-5k': [PayMax[2], PayMin[2]],
            '5-8k': [PayMax[3], PayMin[3]],
            '8-12k': [PayMax[4], PayMin[4]],
            '12-20k': [PayMax[5], PayMin[5]],
            '20-30k': [PayMax[6], PayMin[6]],
            '30k以上': [1000000, PayMin[7]]
        }.get(salary)

    def Map_years(self, WorkYear):
        return {
            '在校生': workYearMapper[0],
            '应届生': workYearMapper[1],
            '1年以内': workYearMapper[2],
            '1-2年': workYearMapper[3],
            '2-3年': workYearMapper[4],
            '3-5年': workYearMapper[5],
            '5-10年': workYearMapper[6],
            '10年以上': workYearMapper[7]

        }.get(WorkYear)

    def Map_year2num(self, WorkYear):
        return {
            workYearMapper[0]: '在校生',
            workYearMapper[1]: '应届生',
            workYearMapper[2]: '1年以内',
            workYearMapper[3]: '1-2年',
            workYearMapper[4]: '2-3年',
            workYearMapper[5]: '3-5年',
            workYearMapper[6]: '5-10年',
            workYearMapper[7]: '10年以上 '

        }.get(WorkYear)

    def FieldChange(self, data):
        data['JobType'] = data.pop('jobType')
        data['JobArea'] = data.pop('jobArea')
        data['JobWorkYears'] = data.pop('workExp')
        data['JobDegree'] = data.pop('edu')
        data['ComTrade'] = data.pop('comTrade')
        data['ComScale'] = data.pop('comScale')
        return data

    def FieldChange_Res(self, data):
        data['Sex'] = data.pop('gender')
        data['WorkArea'] = data.pop('residence')
        data['WishArea'] = data.pop('exceptedArea')
        data['WishJob'] = data.pop('exceptedJob')
        return data


if __name__ == '__main__':
    pass
    # s = js.loads('{"name":"test", "type":{"name":"seq", "parameter":["1", "2"]}}')
    # print(s)
    # print(s["name"])
    # print(s["type"]["name"])
    # print (s["type"]["parameter"][1])
    # a=Search_preprocess()
