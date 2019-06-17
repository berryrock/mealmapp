from django.conf import settings
from django.db import models
from django.utils import timezone


class Page(models.Model):
	url = models.CharField(max_length=200,null=True)
	title = models.CharField(max_length=200)
	desc = models.CharField(max_length=400)
	keywords = models.CharField(max_length=200)
	seo_text = models.TextField()

	def __str__(self):
		return self.title

class Banner(models.Model):
	title = models.CharField(max_length=200)
	active = models.BooleanField()
	desc = models.TextField()
	button_text = models.CharField(max_length=200,default='More')
	link = models.CharField(max_length=200)
	image = models.CharField(max_length=200,null=True)

	def __str__(self):
		return self.title