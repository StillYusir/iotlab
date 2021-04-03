import logging
from SearchAndRecommend.common.MyException import MyException
from SearchAndRecommend.data import PropertiesMapper as pm


class R2jScorce():
    entity_type ="R2J"

    SourceList=["age","degree","wishSalary","perId","workYear"]
    TargetList=["jobAgeMin","jobAgeMax","jobDegree","jobPayMin","jobPayMax","jobId","jobWorkYears"]

    def __init__(self,SourceEntity,TargetEntity,score=0):
        self.score = score
        self.perId=SourceEntity["perId"]
        self.jobId=TargetEntity['jobId']
        if self.perId==None or self.jobId==0:
            raise MyException("perId或jobId为空，抛出异常！")
        self.candAge= int(SourceEntity["age"]) if SourceEntity["age"] else "#"
        self.candDegree = int(SourceEntity['degree']) if SourceEntity['degree'] else "#"
        self.wishSalary = int(SourceEntity['wishSalary']) if SourceEntity['wishSalary'] else "#"
        self.workYear = int(SourceEntity['workYear']) if SourceEntity['workYear'] else "#"

        self.jobAgeMin = int(TargetEntity['jobAgeMin']) if TargetEntity['jobAgeMin'] else "#"
        self.jobAgeMax = int(TargetEntity['jobAgeMax']) if TargetEntity['jobAgeMax'] else "#"
        self.jobDegree = int(TargetEntity['jobDegree']) if TargetEntity['jobDegree'] else "#"
        self.jobPayMin = int(TargetEntity['jobPayMin']) if TargetEntity['jobPayMin'] else "#"
        self.jobPayMax = int(TargetEntity['jobPayMax']) if TargetEntity['jobPayMax'] else "#"
        self.jobWorkYears = int(TargetEntity['jobWorkYears']) if TargetEntity['jobWorkYears'] else "#"

    def verifyParameter(self):
        if self.jobAgeMin=="#":
            self.jobAgeMin=18
        if self.jobAgeMax=='#':
            self.jobAgeMax=60
        if self.jobDegree=='#':
            self.jobDegree=3501
        if self.jobPayMin=='#':
            self.jobPayMin=4000
        if self.jobPayMax=='#':
            self.jobAgeMax=100000
        if self.jobWorkYears=='#':
            self.jobWorkYears=0
        # TODO 这里需要再写参数检验


    def Score(self):
        if self.candAge!="#":
            self.ScoreAge()
        if self.candDegree!='#':
            self.ScoreDegree()
        if self.wishSalary!='#':
            self.ScorePay()
        if self.workYear!='#':
            self.ScoreExperience()
        return self.score

    def ScoreAge(self):
        try:
            if self.candAge in range(self.jobAgeMin,self.jobAgeMax+1):
                self.score+=10
            else:
                self.score-=abs(self.candAge-self.jobAgeMin+(self.jobAgeMax-self.jobAgeMin)//2)*5
        except:
            s="年龄数据异常,"+"perId:"+self.perId+","+"jobId:"+self.jobId
            logging.warn(s)

    def ScoreDegree(self):
        try:
            jobIndex = pm.degreeMapper.index(self.jobDegree)
            candIndex = pm.degreeMapper.index(self.candDegree)
            self.score+=(jobIndex-candIndex)*20
        except:
            s = "学历数据异常," + "perId:" + self.perId + "," + "jobId:" + self.jobId
            logging.warn(s)

    def ScorePay(self):
        try:
            if self.wishSalary<self.jobPayMax:
                self.score+=20
            else:
                self.score+=(self.wishSalary-self.jobPayMax)//10
        except:
            s = "薪资数据异常," + "perId:" + self.perId + "," + "jobId:" + self.jobId
            logging.warn(s)

    def ScoreExperience(self):
        if self.workYear>self.jobWorkYears:
            self.score+=20
        try:
            jobIndex=pm.workYearMapper.index(self.jobWorkYears)
            candIndex = pm.workYearMapper.index(self.workYear)
            self.score+=(jobIndex-candIndex)*20
        except:
            s = "工作经验数据异常," + "perId:" + self.perId + "," + "jobId:" + self.jobId
            logging.warn(s)

