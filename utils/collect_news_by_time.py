# @Time       : 2022/4/16 15:12
# @Author     : HUII
# @File       : collect_news_by_time.py
# @Description:
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
# 开启定时工作
from article.get_news import GetBaiduNews
from article.save_news import save_news

try:
    # 实例化调度器
    scheduler = BackgroundScheduler()
    # 调度器使用DjangoJobStore()
    scheduler.add_jobstore(DjangoJobStore(), "default")


    # 设置定时任务，选择方式为interval，时间间隔为10s
    # 另一种方式为每天固定时间执行任务，对应代码为：
    # @register_job(scheduler, 'cron', day_of_week='mon-fri', hour='9', minute='30', second='10',id='task_time')
    @register_job(scheduler, "interval", minutes=60, id='get_news')
    def my_job():
        # 这里写你要执行的任务
        for news in enumerate(GetBaiduNews().run()):
            save_news(news[1])


    register_events(scheduler)
    scheduler.start()
except Exception as e:
    print(e)
    # 有错误就停止定时器
    scheduler.shutdown()
