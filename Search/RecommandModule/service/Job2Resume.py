from RecommandModule.dao.RecommandEntity import JobField
from RecommandModule.service import J2RScoreFunc as j2r
import json
from operator import methodcaller

class Job2Resume:
    def ReadResume(self,jobId):
        JobInfo = JobField.select().where(JobField.jobId==jobId)
        return JobInfo[0].makeDict()

    #根据职位，查询合适的简历
    def QueryResume(self,JobInfo):
        jobType = self.FilterJob(self,JobInfo)
        querylist = []
        print(jobType)
        for job in jobType:
            query = JobField.select().where((JobField.jobType == job))
            for item in query:
                tmp=item.makeDict()
                querylist.append(tmp.copy())
        return querylist

    #根据职位数据中的JobType列，筛选符合要求的简历
    def FilterResume(self,ResumeInfo):
        return [ResumeInfo["jobType"]]

    #为上一步查到的工作打分，并截取前n个
    def ScoreResume(self,jobInfo,resumeList,n=100):
        print("start sort resumes")
        for resume in resumeList:
            scoreFunc = j2r.R2jScorce(jobInfo, resume)
            score = scoreFunc.Score()
            resume["score"] = score
        resumeList.sort(key=lambda x: -x["score"])
        if len(resumeList) > n:
            resumeList = resumeList[:n]
        res = json.dumps(resumeList, ensure_ascii=False, default=methodcaller, indent=4)
        return res

    def test(self,jobId):
        info = self.ReadResume(self,jobId)
        print(info)

def getRecommandResume(data):
    print("starting recommand resume ...")
    return Job2Resume.test(Job2Resume)
    #return resumeRec.RecommandJob(resumeRec,data)

if __name__=="__main__":
    print("starting test...")
    result = getRecommandResume(111)
