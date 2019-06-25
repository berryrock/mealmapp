from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class AppUser(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE,null=True)
	name = models.CharField(max_length=200,null=True,blank=True)
	surname = models.CharField(max_length=200,null=True,blank=True)
	email = models.EmailField(null=True,blank=True,)
	phone = models.CharField(max_length=20,null=True,blank=True,)
	telegram = models.CharField(max_length=200,null=True,blank=True,)
	registration = models.DateTimeField(auto_now_add=True)
	birthday = models.DateField(null=True,blank=True,)
	length = models.PositiveSmallIntegerField(null=True,blank=True,)
	'''unnecessaried data:
	family = models.ManyToManyField(User,null=True,on_delete=models.SET_NULL,db_index=False)
	gender = models.CharField(max_length=1,choices=(('m', _('Male')),('f', _('Female'))),blank=True,null=True)
	'''

	#def auth(name):

	def __str__(self):
		return str(self.user)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		AppUser.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	instance.appuser.save()

	#Autorization

	#Calculate recommendations

class Device(models.Model):
	TYPE = models.CharField(max_length=200)
	name = models.CharField(max_length=200)
	allowed_users = models.ManyToManyField(AppUser,db_index=False)

	def __str__(self):
		return self.name

class Dish(models.Model):
	name = models.CharField(max_length=200)
	cousine = models.CharField(max_length=200)
	TYPE = models.CharField(max_length=200)
	products = models.TextField(null=True,blank=True,help_text="All words in lowercase and no spaces, use comma as a divider")
	comments = models.CharField(null=True,blank=True,max_length=200)
	avg_point = models.PositiveSmallIntegerField(default=3)

	def __str__(self):
		return self.name

	#Add dish

class Product(models.Model):
	name = models.CharField(max_length=200)
	region = models.CharField(max_length=200)
	TYPE = models.CharField(max_length=200)
	comments = models.CharField(null=True,blank=True,max_length=200)
	avg_point = models.PositiveSmallIntegerField(default=3)

	def __str__(self):
		return self.name

class MealHistory(models.Model):
	date_time = models.DateTimeField(auto_now_add=True)
	user = models.ForeignKey('auth.User',null=True,blank=True,on_delete=models.SET_NULL,db_index=False) #user id
	dish = models.ForeignKey(Dish,null=True,blank=True,on_delete=models.SET_NULL,db_index=False) #dish id
	point = models.NullBooleanField()
	location = models.CharField(blank=True,max_length=200)
	weight = models.PositiveSmallIntegerField(blank=True,null=True)
	acne = models.PositiveSmallIntegerField(blank=True,null=True)
	accepted = models.BooleanField()

	def save(self, *args, **kwargs):
		super(MealHistory, self).save(*args, **kwargs)

	def __str__(self):
		self.date_time = str(self.date_time)[:19]
		return self.date_time

	#Check meal

	#Add meal

	#Point meal

	#Add weight
