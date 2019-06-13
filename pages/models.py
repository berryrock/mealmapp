from django.conf import settings
from django.db import models
from django.utils import timezone


class Page(models.Model):
    title = models.CharField(max_length=200)
    desc = models.CharField(max_length=400)
    keywords = models.CharField(max_length=200)
    seo_text = models.TextField()

    def __str__(self):
        return self.title