from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
from pymongo import MongoClient
class SchedulerConfig:
    #Mongo参数
    host = "127.0.0.1"
    port = 3305
    client = MongoClient(host,port)

    #存储方式(mongodb存储job任务/内存存储)
    jobstores = {
        #"mongo":MongoDBJobStore(collection="job",database="test",client=client),
        "default":MemoryJobStore()

    }
    executors={
        "processpool":ThreadPoolExecutor(10),
        "default": ProcessPoolExecutor(3)
    }
    job_defaults = {
        'coalesce': False,
        'max_instances': 3
    }

def testJob():
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

def mySchedule():
    scheduler = BlockingScheduler(jobstores=SchedulerConfig.jobstores,executors=SchedulerConfig.executors,
                                  job_defaults=SchedulerConfig.job_defaults)
    return scheduler

if __name__=="__main__":
    pass