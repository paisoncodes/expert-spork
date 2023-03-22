from time import sleep
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger


scheduler = BackgroundScheduler()

subscription_trigger = CronTrigger(
    year="*", month="*", day="*", hour="6", minute="30", second="0"
)



