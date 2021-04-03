import logging
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.schedulers.blocking import BlockingScheduler
from logging import getLogger, INFO
from pytz import utc
from datetime import datetime
from pymongo import MongoClient

logger = getLogger(__name__)
logger.setLevel(INFO)


class SchedulerSetting(object):
    # 定义jobstore  使用mongodb存储 job信息
    mongodb_jobstore = MongoDBJobStore(
        # Mongo参数
        host="127.0.0.1",
        port=27017,
        collection="FullPositonDatas",
        database="kunshan",
    )
    # 初始化scheduler
    init_scheduler_options = {
        "jobstores": {
            "default": MemoryJobStore(),
            "mongo": mongodb_jobstore,
        },
        "executors": {
            "processpool": ThreadPoolExecutor(10),  # 默认线程数
            "default": ProcessPoolExecutor(3),   # 默认进程数
        },
        "job_defaults": {
            'coalesce': False,
            'max_instances': 3,
            'misfire_grace_time': 40,  # Job的延迟执行时间 40s
        },
        "timezone": utc
    }

    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filename='./log1.txt',
                        filemode='a+')

    # 定义函数监听事件
    def my_listener(event):
        if event.exception:
            logger.info('The job crashed')
            print(f"{event.job_id}出错了")
        else:
            logger.info('The job worked')
            print(
                "job正常执行:\ncode => {}\njob.id => {}\njobstore=>{}".format(
                    event.code,
                    event.job_id,
                    event.jobstore
                ))

    # 实例化 scheduler
    scheduler = BlockingScheduler(**init_scheduler_options)

    # 给EVENT_JOB_EXECUTED[执行完成job事件]添加回调，这里就是每次Job执行完成了我们就输出一些信息
    scheduler.add_listener(my_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
    scheduler._logger = logging

    # def mySchedule(self):
    #     scheduler = BlockingScheduler(jobstores=SchedulerSetting.jobstores, executors=SchedulerSetting.executors,
    #                                       job_defaults=SchedulerSetting.job_defaults)
    #     return scheduler


# if __name__ == "__main__":
#     scheduler = SchedulerSetting.mySchedule(SchedulerSetting)
#     scheduler.add_job(method_testJob, 'interval', seconds=5)
#     #scheduler.add_job()
#
#     try:
#         scheduler.start()
#     except SystemExit:
#         SchedulerSetting.client.close()
