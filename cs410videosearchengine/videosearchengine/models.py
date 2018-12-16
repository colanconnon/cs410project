from django.db import models


class Video(models.Model):
    video_text = models.TextField(null=True)
    url = models.CharField(max_length=255, null=True)
    gc_uri = models.CharField(max_length=255, null=True)
