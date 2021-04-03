import datetime
import time
from static.area_hash import areaDict


class MappingProperties:
    def edu_change(self, minEdu, maxEdu):
        if minEdu == "":
            minEdu = '3401'
        if maxEdu == "":
            maxEdu = '3407'
        degree_range = {"range": {"Degree": {"gte": minEdu, "lte": maxEdu}}}
        return degree_range

    def age_change(self, minAge, maxAge):
        # 年龄（int）年数[最小年龄]  <  现在的日期 - BirthDate  <  年龄（int）年数[最大年龄]
        #  current_time - maxAge < birthDate < current_time - minAge
        if minAge == "":
            minAge = 0
        if maxAge == "":
            maxAge = 100
        current_time = datetime.datetime.now().strftime('%Y-%m-%d')
        timeArray = time.strptime(current_time, "%Y-%m-%d")
        timeStamp = (time.mktime(timeArray))  # 转化为时间戳
        month_day = time.strftime('%m-%d', time.localtime(timeStamp))
        start_year = int(time.strftime('%Y', time.localtime(timeStamp))) - int(maxAge)
        end_year = int(time.strftime('%Y', time.localtime(timeStamp))) - int(minAge)
        gte_date = '{}-{}'.format(start_year, month_day)
        lte_date = '{}-{}'.format(end_year, month_day)
        age_range = {"range": {"BirthDate": {"gte": gte_date, "lte": lte_date}}}
        return age_range

    def salary_change(self, wish_salary):
        SalaryMapper = ['2301', '2302', '2303', '2304', '2305', '2306', '2307', '2308']
        PayMax = [2000, 3000, 5000, 8000, 12000, 20000, 30000, 100000]
        PayMin = [0, 2000, 3000, 5000, 8000, 12000, 20000, 30000]
        salary_properties = {
            "2301": [PayMax[0], PayMin[0]],
            "2302": [PayMax[1], PayMin[1]],
            "2303": [PayMax[2], PayMin[2]],
            "2304": [PayMax[3], PayMin[3]],
            "2305": [PayMax[4], PayMin[4]],
            "2306": [PayMax[5], PayMin[5]],
            "2307": [PayMax[6], PayMin[6]],
            "2308": [PayMax[7], PayMin[7]]
        }
        if wish_salary in SalaryMapper:
            S_map_list = salary_properties.get(wish_salary)
            jobPayMax, jobPayMin = int(S_map_list[0]), int(S_map_list[1])
            wish_salary_body = {"range": {"WishSalaryMin": {"gte": int(jobPayMin / 1000), "lt": int(jobPayMax / 1000)}}}
            return wish_salary_body
        else:
            print("未传入薪水！")
            return False

    def calculate_age(self, birth):
        birth_d = datetime.datetime.strptime(birth, "%Y-%m-%d")
        today_d = datetime.datetime.now()
        birth_t = birth_d.replace(year=today_d.year)
        if today_d > birth_t:
            age = today_d.year - birth_d.year
        else:
            age = today_d.year - birth_d.year - 1
        return age

    def works_years(self, minWorkYear, maxWorkYear):
        #  minWorkYear  <  current_time - begin_work_date  <  maxWorkYear
        # current_time - maxWorkYear < begin_work_date < current_time - minWorkYear
        if minWorkYear == "":
            minWorkYear = 0
        if maxWorkYear == "":
            maxWorkYear = 100
        current_time = datetime.datetime.now().strftime('%Y-%m-%d')
        timeArray = time.strptime(current_time, "%Y-%m-%d")
        timeStamp = (time.mktime(timeArray))  # 转化为时间戳
        month_day = time.strftime('%m-%d', time.localtime(timeStamp))
        start_year = int(time.strftime('%Y', time.localtime(timeStamp))) - int(maxWorkYear)
        end_year = int(time.strftime('%Y', time.localtime(timeStamp))) - int(minWorkYear)
        gte_date = '{}-{}'.format(start_year, month_day)
        lte_date = '{}-{}'.format(end_year, month_day)
        workYears_range = {"range": {"BeginWorkDate": {"gte": gte_date, "lte": lte_date}}}
        return workYears_range

    def areaExpansion(self, area):
        return areaDict[area]


mp = MappingProperties()

'''
2k以下
2k-3k
3k-5k
5k-8k
8k-12k
12k-20k
20k-30k
30以上
'''

if __name__ == '__main__':
    birthDate = '2010-03-09'
    age = mp.calculate_age(birthDate)
    print(age)
