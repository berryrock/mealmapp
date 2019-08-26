from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

def point_update(new_point,old_point):
	if new_point == 1:
		old_point += 2
	elif new_point == 0:
		old_point -= 1
	else:
		old_point += 1
	return old_point

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

	def get_vector(self):
		region_vector = RegionVector.objects.order_by('-pk')[:1]
		dishes = region_vector.values_list("dishes", flat=True)[0]
		dishes = dishes.replace("]", "").replace("[", "").replace("""'""", "")
		dishes = dishes.split(',')
		i = 0
		vector = ""
		for dish in dishes:
			if dish[0] == " ":
				dish = dish[1:]
			if i < 3:
				vector += dish
				vector += ","
				i += 1
			else:
				break

		print(vector)
		result = {'id': self.id, 'vector': vector}
		return result

	def get_dish_info(self, dish):
		string = "This feature still in development"
		return string

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
	name = models.CharField(max_length=200, primary_key=True)
	cousine = models.CharField(max_length=200,null=True)
	TYPE = models.CharField(max_length=200,null=True)
	tags = models.CharField(max_length=200,null=True,blank=True)
	products = models.TextField(null=True,blank=True,help_text="All words in lowercase and no spaces, use comma as a divider")
	carbs = models.CharField(max_length=200,null=True,blank=True)
	fats = models.CharField(max_length=200,null=True,blank=True)
	proteins = models.CharField(max_length=200,null=True,blank=True)
	kcal = models.CharField(max_length=200,null=True,blank=True)
	comments = models.CharField(null=True,blank=True,max_length=200)
	avg_point = models.PositiveSmallIntegerField(default=30)
	frequency = models.CharField(max_length=200,default=30)
	specials_rules = models.CharField(max_length=200,null=True,blank=True)
	region = models.ForeignKey(Region,blank=True,null=True,on_delete=models.SET_NULL,db_index=False)
	parsed = models.BooleanField(default=False)

	def __str__(self):
		return self.name

class Product(models.Model):
	name = models.CharField(max_length=200)
	TYPE = models.CharField(max_length=200,null=True,blank=True)
	avg_point = models.PositiveSmallIntegerField(default=30)
	kcal = models.CharField(max_length=200,null=True,blank=True)
	proteins = models.CharField(max_length=200,null=True,blank=True)
	fats = models.CharField(max_length=200,null=True,blank=True)
	carbs = models.CharField(max_length=200,null=True,blank=True)
	comments = models.CharField(null=True,blank=True,max_length=200)
	season = models.CharField(max_length=200,null=True,blank=True)

	def __str__(self):
		return self.name

class Preference(models.Model):
	PRODUCT = 'PR'
	DISH = 'DS'
	OBJECT_TYPE_CHOICES = [
		(DISH, 'Dish'),
		(PRODUCT, 'Product'),
	]

	TYPE = models.CharField(max_length=2,choices=OBJECT_TYPE_CHOICES,default=DISH,)
	user = models.ForeignKey(AppUser,on_delete=models.CASCADE)
	dish = models.ForeignKey(Dish,on_delete=models.CASCADE,null=True,blank=True)
	product = models.ForeignKey(Product,on_delete=models.CASCADE,null=True,blank=True)
	preference = models.PositiveSmallIntegerField(default=30)
	frequency = models.PositiveSmallIntegerField(default=1)
	weight_effect = models.PositiveSmallIntegerField(default=30)
	last_meal_date = models.DateField(auto_now=False,auto_now_add=False,blank=True)

class MealHistory(models.Model):
	date_time = models.DateTimeField(auto_now_add=True)
	dish = models.ForeignKey(Dish,null=True,blank=True,on_delete=models.SET_NULL,db_index=False) #dish id
	point = models.NullBooleanField()
	location = models.CharField(max_length=200,default='russia')
	user = models.ForeignKey('auth.User',null=True,blank=True,on_delete=models.SET_NULL,db_index=False) #user id
	weight = models.CharField(max_length=5,blank=True,null=True)
	acne = models.PositiveSmallIntegerField(blank=True,null=True)
	accepted = models.BooleanField(default=False)

	def save(self, *args, **kwargs):
		'''first scenario meal added
		that means program should take dish name and products and update their point and frequency'''
		if self.dish:
			print(self.dish)
			dish = Dish.objects.filter(name=self.dish,region=self.location)
			print(dish)
			dish_point = dish.values_list("avg_point", flat=True)[0]
			dish_products = dish.values_list("products", flat=True)[0]
			dish_point = point_update(self.point,dish_point)
			Dish.objects.filter(name=self.dish).update(avg_point=dish_point)
			products = dish_products.split(',')
			for product in products:
				product_point = Product.objects.filter(name=product)
				point = product_point.values_list("avg_point", flat=True)[0]
				point = point_update(self.point,point)
				Product.objects.filter(name=product).update(avg_point=point)
		'''first scenario weight added
		program should update user weight'''
		if self.weight:
			AppUser.objects.filter(user=self.user).update(weigth=self.weight)
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
