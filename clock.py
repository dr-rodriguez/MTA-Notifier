from apscheduler.schedulers.blocking import BlockingScheduler
import notifier

sched = BlockingScheduler()

# EDT/EST is 4/5 hours ahead of UTC, which is what Heroku runs in

# Morning check
@sched.scheduled_job('cron', day_of_week='mon-fri', hour=13, minute=55)
def scheduled_job_morning():
    m = notifier.Notifier()
    m.verbose = False
    m.get_status(['123', 'ACE'])

    m.send_email_message()

# Afternoon check
@sched.scheduled_job('cron', day_of_week='mon-fri', hour=21, minute=30)
def scheduled_job_morning():
    m = notifier.Notifier()
    m.verbose = False
    m.get_status(['123', 'ACE'])

    m.send_email_message()

# Weekend planner
@sched.scheduled_job('cron', day_of_week='sat', hour=14, minute=30)
def scheduled_job_weekend():
    m = notifier.Notifier()
    m.verbose = False
    m.get_status(['123', 'ACE'], ['GOOD SERVICE', 'DELAYS'])  # Don't notify about delays in addition to good service

    m.send_email_message('MTA Weekend Notifier')  # Explicitly set subject

sched.start()