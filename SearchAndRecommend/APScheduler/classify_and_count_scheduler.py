import sys
# sys.path.append('/home/iotlab/Search/')
sys.path.append('/project/iotlab-dev/iotlab-dev/')

from Search.SearchAndRecommend.APScheduler.extract_static_small_classify_positons import tiqu_small_class_index
from Search.SearchAndRecommend.APScheduler.SchedulerConfig import SchedulerSetting
from datetime import datetime
from Search.SearchAndRecommend.PostionDataSynchronization.full_extract_datas import full_synchronization

scheduler = SchedulerSetting.scheduler


def ttest_time():
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
# 测试用的方法--每隔5s打印一次时间

def method_testJob():
    if scheduler.get_job("ttest_time"):
        # 存在的话，先删除
        scheduler.remove_job("ttest_time")

    scheduler.add_job(func=ttest_time, trigger='interval',
                      id='ttest_time',
                      seconds=3,
                      jobstore="mongo",
                      replace_existing=True
                      )

# 全量同步方法
def full_position_data():
    if scheduler.get_job("full_synchronization"):
        # 存在的话，先删除
        scheduler.remove_job("full_synchronization")

    # 添加全量同步任务  暂定为 每周一凌晨2点半 执行
    scheduler.add_job(func=full_synchronization, trigger='cron',
                      id='full_synchronization',
                      day_of_week='Mon', hour='2', minute='30',
                      jobstore="mongo", executor="default",
                      replace_existing=True
                      )

# 初始化小类别中职位的数量
def init_small_position_count():
    # 从全量同步下来的json文件中提取统计各小类中职位的数量
    if scheduler.get_job("tiqu_small_class_index"):
        # 存在的话，先删除
        scheduler.remove_job("tiqu_small_class_index")

    # 添加提取类别中职位数量静态表任务  暂定为 每周一凌晨4点40分 执行
    scheduler.add_job(func=tiqu_small_class_index, trigger='cron',
                      id='tiqu_small_class_index',
                      day_of_week='Thu', hour='11', minute='02',
                      jobstore="mongo", executor="default",
                      replace_existing=True
                      )


# 增量同步方法
def increase_synchronization():
    pass


if __name__ == "__main__":
    # TODO 讨论增量同步时间间隔
    # full_position_data()
    # init_small_position_count()
    method_testJob()
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown(wait=False)
