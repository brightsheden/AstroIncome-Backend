import os
from celery import Celery


"""os.environ.setdefault('DJANGO_SETTINGS_MODULE',
'trustfund.settings'
)
app=Celery('trustfund',broker='memory://')
app.config_from_object('django.conf:settings',namespace='CELERY')
app.autodiscover_task()"""