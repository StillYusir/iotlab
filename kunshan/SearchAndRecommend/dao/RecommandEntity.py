import sys
import pathlib

sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))
__author__="常思维"

from peewee import *
from SearchAndRecommend.dao.DatabaseConfig import kunshan_db
from SearchAndRecommend.common.MyException import *

class BaseModel(Model):
    class Meta:
        database = kunshan_db

class ResumeField(BaseModel):
    perId = CharField(primary_key=True,column_name="Perid")
    wishJobType = CharField(column_name="WishJobType")
    degree = CharField(column_name="Degree")
    sex = CharField(column_name="Sex")
    wishSalary = CharField(column_name="WishSalary")
    workYear = CharField(column_name="WorkYear")
    age = CharField(column_name="Age")
    wishArea = CharField(column_name="WishArea")
    updateDate = CharField(column_name="UpdateDate")
    score = 0
    ResumeInfo={}

    def makeDict(self):
        try:
            if self.perId is not None:
                self.ResumeInfo["perId"]=self.perId
            else:
                raise MyException("perId错误")
        except MyException as e:
            print(e.message)
        self.ResumeInfo["wishJobType"] = self.wishJobType
        self.ResumeInfo["degree"]=self.degree
        self.ResumeInfo["sex"]=self.sex
        self.ResumeInfo["wishSalary"]=self.wishSalary
        self.ResumeInfo["workYear"]=self.workYear
        self.ResumeInfo["age"]=self.age
        self.ResumeInfo["wishArea"]=self.wishArea
        self.ResumeInfo["updateDate"]=self.updateDate
        self.ResumeInfo["score"]=self.score
        return self.ResumeInfo

    def toString(self):
        print(self.perId,"\t",self.wishJobType,"\t",self.degree,"\t",self.sex,"\t",
              self.wishSalary,"\t",self.workYear,"\t",self.age,"\t",self.wishArea
              , "\t",self.updateDate)
    class Meta:
        table_name = "简历基本信息"


class JobField(BaseModel):
    jobId = CharField(primary_key=True,column_name="JobID")
    jobName = CharField(column_name="JobName")
    jobWorkYears = CharField(column_name="JobWorkYears")
    jobSex = CharField(column_name="JobSex")
    jobType = CharField(column_name="JobType")
    jobDegree = CharField(column_name="JobDegree")
    jobArea = CharField(column_name="JobArea")
    jobPayMin = CharField(column_name="JobPayMin")
    jobPayMax = CharField(column_name="JobPayMax")
    jobAgeMin = CharField(column_name="JobAgeMin")
    jobAgeMax = CharField(column_name="JobAgeMax")
    jobTopEndDate = CharField(column_name="JobTopEndDate")
    isDel = CharField(column_name="isDel")
    ResumeInfo={}
    score=0

    def makeDict(self):
        try:
            if self.jobId is not None:
                self.ResumeInfo["jobId"]=self.jobId
            else:
                raise MyException("jobId错误")
        except MyException as e:
            print(e.message)
        self.ResumeInfo["jobName"] = self.jobName
        self.ResumeInfo["jobWorkYears"]=self.jobWorkYears
        self.ResumeInfo["jobSex"]=self.jobSex
        self.ResumeInfo["jobType"]=self.jobType
        self.ResumeInfo["jobDegree"]=self.jobDegree
        self.ResumeInfo["jobArea"]=self.jobArea
        self.ResumeInfo["jobPayMin"]=self.jobPayMin
        self.ResumeInfo["jobPayMax"]=self.jobPayMax
        self.ResumeInfo["jobAgeMin"]=self.jobAgeMin
        self.ResumeInfo["jobAgeMax"]=self.jobAgeMax
        self.ResumeInfo["jobTopEndDate"]=self.jobTopEndDate
        self.ResumeInfo["isDel"]=self.isDel
        self.ResumeInfo["score"]=self.score
        return self.ResumeInfo

    def toString(self):
        print(self.jobId,"\t",self.jobName,"\t",self.jobWorkYears,"\t",self.jobSex,"\t",
              self.jobType,"\t",self.jobDegree,"\t",self.jobArea,"\t",self.jobPayMin
              , "\t",self.jobAgeMax, "\t",self.jobTopEndDate,"\t",self.isDel, "\t",self.score)
    class Meta:
        table_name="职位" \
                   "样本"

if __name__ == "__main__":
    pass
    # query = (JobField.select().distinct())
    # category_list = [row for row in query]
    # print(type(category_list[0]))
    # for item in category_list:
    #     #print(item)
    #     print(JobField.get(JobField.jobId==item))
    #query = JobField.select().where(JobField.jobSex=="3201")
