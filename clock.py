from apscheduler.schedulers.blocking import BlockingScheduler
import notifier

sched = BlockingScheduler()

# Eastern is 4 hours ahead of UTC, which is what Heroku runs in

# Afternoon check
@sched.scheduled_job('cron', day_of_week='mon-fri', hour=20, minute=30)
def scheduled_job():
    m = notifier.Notifier()
    m.verbose = False  # Ensure verbosity is set to False
    m.get_status(['123', 'ACE'])

    m.send_email_message()

# Morning check
@sched.scheduled_job('cron', day_of_week='mon-fri', hour=12, minute=55)
def scheduled_job():
    m = notifier.Notifier()
    m.verbose = False
    m.get_status(['123', 'ACE'])

    m.send_email_message()

sched.start()