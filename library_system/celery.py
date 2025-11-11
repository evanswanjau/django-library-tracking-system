import os
from celery import Celery
# from celery.schedule import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_system.settings')

app = Celery('library_system')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# add cron job usin beat
#TODO: Add Daily Reminder
# app.conf.beat_schedule = {
#   'overdue_loan_daily_reminder':{
#     'task': 'library.tasks.check_overdue_loans',
#     'schedule': crontab(hour=8, minute=0)
#   }
# }
