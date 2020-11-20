from RecommandModule.dao.RecommandEntity import ResumeField,JobField
import json
from SearchAndRecommend.service import CleanData as cd
from operator import methodcaller
from RecommandModule.service import R2JScoreFunc as r2j

class Resume2Job:
    #测试用，功能为从数据库中拉取简历信息
    def ReadResume(self,perid):
        ResumeInfo = ResumeField.select().where(ResumeField.perId==perid)
        return ResumeInfo[0].makeDict()
    #根据简历，查询合适的工作
    def QueryJob(self,ResumeInfo):
        wishArea,wishJob = self.FilterJob(self,ResumeInfo)
        querylist = []
        print(wishJob)
        for job in wishJob:
            #有很多jobtype是没有的，所以这里这里指定一个type先试试
            query = JobField.select().where((JobField.jobType=="211120"))
            #query = JobField.select().where((JobField.jobType==job))
            for item in query:
                tmp=item.makeDict()
                querylist.append(tmp.copy())
        return querylist



    #为上一步查到的工作打分，并截取前n个
    def ScoreJob(self,resumeInfo,jobList,n=100):
        print("start sort jobs")
        for item in jobList:
            scoreFunc = r2j.R2jScorce(resumeInfo, item)
            score = scoreFunc.Score()
            item["score"]=score
        jobList.sort(key=lambda x:-x["score"])
        if len(jobList)>n:
            jobList=jobList[:n]
        res=json.dumps(jobList,ensure_ascii=False,default=methodcaller,indent=4)
        return res

    #清洗数据接口，暂时只对wishJobType和wishArea清洗
    def FilterJob(self,ResumeInfo):
        if len(ResumeInfo["wishJobType"])>=6:
            wishJobType = cd.CleanWishJobType(self,ResumeInfo["wishJobType"])
        else:
            wishJobType=list(ResumeInfo["wishJobType"])
        if len(ResumeInfo["wishArea"])>=7:
            wishArea = cd.CleanWishArea(self,ResumeInfo["wishArea"])
        else:
            wishArea=list(ResumeInfo["wishArea"])
        return wishArea,wishJobType

    def RecommandJob(self,resumeData):
        querylist = self.QueryJob(self,resumeData)
        result = self.ScoreJob(resumeData,querylist)
        print(result)
        return result

    def test(self):
        resumeInfo = self.ReadResume(self,"2089489")
        print(resumeInfo)
        querylist = self.QueryJob(self,resumeInfo)
        res=self.ScoreJob(self,resumeInfo,querylist)
        print(res)
        return res

def getRecommandJob(data):
    print("starting recommand job ...")
    return Resume2Job.test(Resume2Job)
    #return resumeRec.RecommandJob(resumeRec,data)

if __name__=="__main__":
    print("starting test...")
    result = getRecommandJob(111)