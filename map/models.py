from django.conf import settings
from django.db import models
from django.forms import widgets
from django.utils import timezone

class User(models.Model):
	ext_id = models.CharField(max_length=200,unique=True)
	name = models.CharField(max_length=200,null=True)
	surname = models.CharField(max_length=200,null=True)
	email = models.EmailField(null=True)
	telephone = widgets.NumberInput()
	telegram = models.CharField(max_length=200,null=True)
	registration = models.DateTimeField(auto_now_add=True)
	birthday = models.DateField(null=True)
	length = models.PositiveSmallIntegerField(null=True,)
	'''unnecessaried data:
	family = models.ManyToManyField(User,null=True,on_delete=models.SET_NULL,db_index=False)
	'''

	#def auth(name):

	def __str__(self):
		return self.name

	#Autorization

	#Calculate recommendations

class Device(models.Model):
	TYPE = models.CharField(max_length=200)
	name = models.CharField(max_length=200)
	allowed_users = models.ManyToManyField(User,db_index=False)

	def __str__(self):
		return self.name

class Dish(models.Model):
	name = models.CharField(max_length=200)
	cousine = models.CharField(max_length=200)
	TYPE = models.CharField(max_length=200)
	products = models.TextField(null=True,help_text="All words in lowercase and no spaces, use comma as a divider")
	comments = models.CharField(max_length=200)
	avg_point = models.PositiveSmallIntegerField(default=3)

	def __str__(self):
		return self.name

	#Add dish

class Product(models.Model):
	name = models.CharField(max_length=200)
	region = models.CharField(max_length=200)
	TYPE = models.CharField(max_length=200)
	comments = models.CharField(max_length=200)
	avg_point = models.PositiveSmallIntegerField(default=3)

	def __str__(self):
		return self.name

class MealHistory(models.Model):
	date_time = models.DateTimeField(auto_now_add=True)
	user = models.ForeignKey(User,null=True,on_delete=models.SET_NULL,db_index=False) #user id
	dish = models.ForeignKey(Dish,null=True,on_delete=models.SET_NULL,db_index=False) #dish id
	point = models.NullBooleanField()
	location = models.CharField(max_length=200)
	weight = models.PositiveSmallIntegerField()
	acne = models.PositiveSmallIntegerField()
	accepted = models.BooleanField()

	#Check meal

	#Add meal

	#Point meal

	#Add weight
