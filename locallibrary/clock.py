from apscheduler.schedulers.blocking import BlockingScheduler
from rq import Queue
from worker import conn
import os
import django
from utils import removeLinks

"""
@sched.scheduled_job('cron', day_of_week='mon-fri', hour=17)
def scheduled_job():
    print('This job is run every weekday at 5pm.')
	
"""
if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'locallibrary.settings')
    django.setup()
    q = Queue(connection=conn)
    sched = BlockingScheduler()
    @sched.scheduled_job('interval', minutes=1)
    def timed_job():
        result = q.enqueue(removeLinks)
        print('This job is run every 1 minute.')
    sched.start()
else:
    def start_jobs():
        q = Queue(connection=conn)
        sched = BlockingScheduler()
        @sched.scheduled_job('interval', minutes=1)
        def timed_job():
            result = q.enqueue(removeLinks)
            print('This job is run every 1 minute.')
        sched.start()