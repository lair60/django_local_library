import os
import django
from apscheduler.schedulers.blocking import BlockingScheduler
from rq import Queue

"""
@sched.scheduled_job('cron', day_of_week='mon-fri', hour=17)
def scheduled_job():
    print('This job is run every weekday at 5pm.')
	
"""
if __name__ == '__main__':
    from utils import removeLinks   
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
    import redis
    from locallibrary.utils import removeLinks
    def start_jobs():
        redis_url = os.environ.get('REDISTOGO_URL', 'redis://localhost:6379')
        conn = redis.from_url(redis_url)
        q = Queue(connection=conn)
        sched = BlockingScheduler()
        @sched.scheduled_job('interval', minutes=1)
        def timed_job():
            result = q.enqueue(removeLinks)
            print('This job is run every 1 minute.')
        sched.start()