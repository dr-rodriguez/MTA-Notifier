from apscheduler.schedulers.blocking import BlockingScheduler
import notifier

sched = BlockingScheduler()

@sched.scheduled_job('cron', day_of_week='mon-fri', hour=17)
def scheduled_job():
    m = notifier.Notifier()
    m.get_status(['123', 'ACE'])
    send_email = True

    if send_email:
        m.send_email_message()

sched.start()