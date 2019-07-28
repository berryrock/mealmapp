from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Region(models.Model):
	name = models.CharField(max_length=200, primary_key=True)
	public_name = models.CharField(max_length=200,blank=True)
	borders = models.TextField(blank=True)

	def __str__(self):
		return self.name

class AppUser(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE,null=True)
	registration = models.DateTimeField(auto_now_add=True)
	name = models.CharField(max_length=200,null=True,blank=True)
	surname = models.CharField(max_length=200,null=True,blank=True)
	email = models.EmailField(null=True,blank=True,)
	phone = models.CharField(max_length=20,null=True,blank=True,)
	region = models.ForeignKey(Region,blank=True,null=True,on_delete=models.SET_NULL,db_index=False)
	length = models.PositiveSmallIntegerField(null=True,blank=True,)
	birthday = models.DateField(null=True,blank=True,)
	weigth = models.PositiveSmallIntegerField(null=True,blank=True,)
	telegram = models.CharField(max_length=200,null=True,blank=True,)
	
	def __str__(self):
		return str(self.user)

	@receiver(post_save, sender=User)
	def create_user_profile(sender, instance, created, **kwargs):
		if created:
			AppUser.objects.create(user=instance)

	@receiver(post_save, sender=User)
	def save_user_profile(sender, instance, **kwargs):
		instance.appuser.save()

class Device(models.Model):
	TYPE = models.CharField(max_length=200)
	name = models.CharField(max_length=200)
	allowed_users = models.ForeignKey(AppUser,null=True,blank=True,on_delete=models.SET_NULL,db_index=False)

	def __str__(self):
		return self.name

class Dish(models.Model):
	name = models.CharField(max_length=200)
	cousine = models.CharField(max_length=200)
	TYPE = models.CharField(max_length=200)
	tags = models.CharField(max_length=200,null=True,blank=True)
	specials_cousine = models.CharField(max_length=200,null=True,blank=True)
	products = models.TextField(null=True,blank=True,help_text="All words in lowercase and no spaces, use comma as a divider")
	comments = models.CharField(null=True,blank=True,max_length=200)
	region = models.ForeignKey(Region,blank=True,null=True,on_delete=models.SET_NULL,db_index=False)
	avg_point = models.PositiveSmallIntegerField(default=30)
	frequency = models.CharField(max_length=200,default=30)
	kcal = models.CharField(max_length=200,null=True,blank=True)
	proteins = models.CharField(max_length=200,null=True,blank=True)
	fats = models.CharField(max_length=200,null=True,blank=True)
	carbs = models.CharField(max_length=200,null=True,blank=True)

	def __str__(self):
		return self.name

class Product(models.Model):
	name = models.CharField(max_length=200)
	group = models.CharField(max_length=200)
	avg_point = models.PositiveSmallIntegerField(default=30)
	kcal = models.CharField(max_length=200,null=True,blank=True)
	proteins = models.CharField(max_length=200,null=True,blank=True)
	fats = models.CharField(max_length=200,null=True,blank=True)
	carbs = models.CharField(max_length=200,null=True,blank=True)
	comments = models.CharField(null=True,blank=True,max_length=200)
	season = models.CharField(max_length=200,null=True,blank=True)

	def __str__(self):
		return self.name

class MealHistory(models.Model):
	date_time = models.DateTimeField(auto_now_add=True)
	dish = models.ForeignKey(Dish,null=True,blank=True,on_delete=models.SET_NULL,db_index=False) #dish id
	point = models.NullBooleanField()
	location = models.CharField(max_length=200,blank=True)
	user = models.ForeignKey('auth.User',null=True,blank=True,on_delete=models.SET_NULL,db_index=False) #user id
	weight = models.PositiveSmallIntegerField(blank=True,null=True)
	acne = models.PositiveSmallIntegerField(blank=True,null=True)
	accepted = models.BooleanField()

	def save(self, *args, **kwargs):
		super(MealHistory, self).save(*args, **kwargs)

	def __str__(self):
		self.date_time = str(self.date_time)[:19]
		return self.date_time

class RegionVector(models.Model):
	date_time = models.DateTimeField(auto_now=True)
	dishes = models.TextField()
	region = models.ForeignKey(Region,null=True,blank=True,default='russia',on_delete=models.SET_NULL,db_index=False)

	def save(self, *args, **kwargs):
		if not self.id:
			self.date_time = models.DateTimeField(auto_now_add=True)
		return super(RegionVector, self).save(*args, **kwargs)

	def __str__(self):
		self.date_time = str(self.date_time)[:19]
		return self.date_time
