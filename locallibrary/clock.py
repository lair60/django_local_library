from apscheduler.schedulers.blocking import BlockingScheduler
from rq import Queue
from worker import conn
from utils import count_words_at_url

q = Queue(connection=conn)
sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=1)
def timed_job():
    result = q.enqueue(removeLinks)
    print('This job is run every 1 minute.')
"""
@sched.scheduled_job('cron', day_of_week='mon-fri', hour=17)
def scheduled_job():
    print('This job is run every weekday at 5pm.')
	
"""

sched.start()