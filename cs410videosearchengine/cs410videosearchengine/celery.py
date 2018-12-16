import os
from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cs410videosearchengine.settings")

app = Celery("cs410videosearchengine")
app.config_from_object("django.conf:settings")
app.autodiscover_tasks()
