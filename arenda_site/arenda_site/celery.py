from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

import arenda_site.settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "arenda_site.settings")

app = Celery("arenda_site")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.beat_schedule = {
    'Delete Message': {
        'task': "site_app.tasks.deleting_task",
        "schedule": crontab(),#crontab(minute=0, hour=0),
    },
}
# app.conf.timezone = arenda_site.settings.TIME_ZONE
app.autodiscover_tasks()

