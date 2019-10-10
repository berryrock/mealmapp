from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime
import json


'''USER PREFERENCE FUNCTIONS'''
def point_update(new_point,old_point):
	if new_point == 1:
		old_point += 2
	elif new_point == 0:
		old_point -= 1
	else:
		old_point += 1
	return old_point

def check_product_preference(type,product_preference_list,prefered_products,unprefered_products):
	product_preference = product_preference_list.values_list(type,flat=True)
	if product_preference > 35:
		prefered_products.append(product)
	elif product_preference < 25:
		unprefered_products.append(product)
	return (product_preference,prefered_products,unprefered_products)

def calculate_avg_preference(preferences):
	preference_numbres = 0
	preference_summ = 0
	for preference in preferences:
		frequency_summ += preference 
		frequency_numbers += 1
	avg_number = frequency_summ / frequency_numbers
	return avg_number



'''VECTORS CALCULATION FUNCTIONS'''
def lower_dish_points(dish_name,user):
	dish_data = Dish.objects.get(name=dish_name)
	try:
		dish = Preference.objects.get(dish=dish_data,user=user)
		dish.preference = point_update(0,dish.preference)
		dish.save()
	except:
		Preference.objects.create(TYPE='DS',dish=dish_data,user=user)
		products = dish_data.products.split(',')
		for product in products:
			try:
				product_preference = Preference.objects.get(product=product,user=user)
			except:
				product_obj = Product.objects.get(name=product)
				Preference.objects.create(TYPE='PR',product=product_obj,user=user)

def check_entry(item,LIST):
	num_entries = 0
	item = str(item)
	LIST = str(LIST)
	try:
		LIST.index(item)
		num_entries += 1 
	except ValueError:
		pass
	return num_entries

def get_list_of(dishes,prefered_products):
	dish_list = {}
	for dish_preference in dishes:
		dish = Dish.objects.get(name=dish_preference.dish)
		num_pref_prod = 0
		for product_preference in prefered_products:
			product = Product.objects.get(name=product_preference.product)
			num_pref_prod += check_entry(product,dish.products)
		if num_pref_prod > 1:
			dish_list.update({dish.name: (dish_preference.preference,dish_preference.frequency,dish_preference.weight_effect)})
	return dish_list

def calculate_points_for(dish_list):
	pointed_dishes = {}
	dishes = dish_list.keys()
	for dish in dishes:
		points = 0
		try:
			preferences = dish_list.get(dish)
			preference = preferences[0]
			frequency = preferences[1]
			weight_effect = preferences[2]
			points = (preference + weight_effect) / frequency
		except:
			pass
		pointed_dishes.update({dish: points})
	return pointed_dishes

def calculate_location_vector_for(region='russia',string=True):
	location_vector = {}
	print(timezone.now(), "/Starting region vector calculation/")
	pref_products = Product.objects.order_by('avg_point').reverse()[:20]
	frequent_dishes = Dish.objects.order_by('frequency').reverse()[:500]
	for dish in frequent_dishes:
		points = 0
		num_pref_prod = 0
		for product in pref_products:
			num_pref_prod += check_entry(product,dish.products)
		if num_pref_prod > 1:
			points = int(dish.avg_point) + (int(dish.frequency) / 30)
			location_vector.update({dish.name: points})
		dish.frequency = str(int(dish.frequency) - 1)
		dish.save()
	#print(timezone.now(), location_vector)
	if string:
		location_vector = str(location_vector).replace("'",'''"''')
	return location_vector

def calculate_preference_vector_for(user):
	print(timezone.now(), "/Starting user vector calculation/")
	with_pref_products = Preference.objects.filter(user=user,TYPE='PR').order_by('-preference')[:20]
	dishes = Preference.objects.filter(user=user,TYPE='DS')
	dish_list = get_list_of(dishes,with_pref_products)
	preference_vector = calculate_points_for(dish_list)
	print(timezone.now(), preference_vector)
	return preference_vector


'''DJANGO MODELS'''

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
	phone = models.CharField(max_length=20,null=True,blank=True)
	region = models.ForeignKey(Region,blank=True,null=True,on_delete=models.SET_NULL,db_index=False)
	length = models.CharField(max_length=6,null=True,blank=True)
	birthday = models.DateField(null=True,blank=True)
	weigth = models.CharField(max_length=6,null=True,blank=True)
	telegram = models.CharField(max_length=200,null=True,blank=True)
	
	def __str__(self):
		return str(self.user)

	def get_vector(self):
		prefered_dishes={}
		preference_vector=[]
		user_prefered_dishes = calculate_preference_vector_for(self)
		if user_prefered_dishes == {}:
			user_prefered_dishes = calculate_location_vector_for(self.region,False)
		else:
			region_vector_object = RegionVector.objects.filter(region=self.region).order_by('pk').reverse()[0]
			try:
				region_prefered_dishes = json.loads(region_vector_object.dishes)
			except AttributeError:
				region_prefered_dishes = {}
			prefered_dishes.update(region_prefered_dishes)
		prefered_dishes.update(user_prefered_dishes)
		list_of_prefered_dishes = list(prefered_dishes.items())
		list_of_prefered_dishes.sort(key=lambda i: i[1])
		m = 0
		for i in list_of_prefered_dishes:
			if m < 10:
				preference_vector.append(i[0])
				m += 1
			else:
				break
		print(preference_vector)

		n = 0
		for choosen_dish in preference_vector:
			n += 1
			lower_dish_points(choosen_dish,self)
			if n > 2:
				break
		string = ','.join(preference_vector)
		result = {'id': self.id, 'vector': string}
		return result

	def get_dish_info(self, dish, user):
		#ALL VARIABLES LIST
		message = ""
		sentences = 0
		#PRODUCT VARIABLES
		products_preference_number = 30
		products_frequency_number = 1
		products_preference = []
		prefered_products = []
		unprefered_products = []
		products_frequency = []
		unfrequent_products = []
		frequent_products = []
		#DISH INFO PROCESS FLOW
		dish = Dish.objects.get(name=dish)
		#CREATE UNACCEPTED MEALHISTORY 
		MealHistory.objects.create(dish=dish,user=user)
		try:
			preference = Preference.objects.get(user=user,dish=dish)
			dish_preference = preference.preference
			dish_frequency = preference.frequency

			try:
				product_list = dish.products
				products = product_list.split(',')
				for product in products:

					try:
						product_preference_list = Preference.objects.get(user=user,product=product)
						#PREFERENCES
						products_preferences = check_product_preference('preference',product_preference_list,prefered_products,unprefered_products)
						products_preference.append(products_preferences[0])
						try:
							prefered_products.append(products_preferences[1])
						except:
							pass
						try:
							unprefered_products.append(products_preferences[2])
						except:
							pass
						products_preferences = check_product_preference('frequency',product_preference_list,prefered_products,unprefered_products)
						#FREQUENCY
						products_frequency.append(products_preferences[0])
						try:
							frequent_products.append(products_preferences[2])
						except:
							pass
					except Preference.DoesNotExist:
						avg_product = Product.objects.get(name=product)
						avg_product_preference = check_product_preference('avg_point',avg_product,prefered_products,unprefered_products)
						try:
							prefered_products.append(avg_product_preference[1])
						except:
							pass
						try:
							unprefered_products.append(avg_product_preference[2])
						except:
							pass
						products_preference.append(avg_product_preference[0])
						products_frequency.append(1)

				products_preference_number = calculate_avg_preference(products_preference)
				products_frequency_number = calculate_avg_preference(products_frequency)
			except:
				#print("No products")
				pass

		except Preference.DoesNotExist:
			dish_preference = dish.avg_point
			dish_frequency = 1
		
		if (dish_preference > 35) or (products_preference_number > 35):
			message += "that dish should be liked by you"
			sentences += 1
			if len(prefered_products) == 1:
				message += "and especially {}".format(prefered_products[0])
			elif len(prefered_products) > 1:
				message += "and especially {}".format(prefered_products[0])
				for prod in prefered_products:
					message += ", {}".format(prod)
		elif (dish_preference < 25) or (products_preference_number < 25):
			message += "you will dislike that dish"
			sentences += 1
			if len(unprefered_products) == 1:
				message += "and especially {}".format(unprefered_products[0])
			elif len(unprefered_products) > 1:
				message += "and especially {}".format(unprefered_products[0])
				for prod in unprefered_products:
					message += ", {}".format(prod)

		if dish_frequency > 3:
			if sentences > 0:
				message += ". But "
			message += "you eat it too often"
			sentences += 1
		dish_weight_effect = preference.weight_effect
		if dish_weight_effect > 35:
			if sentences > 0:
				message += ". "
			message += "It's too bad for your weight"
		if dish_weight_effect < 25:
			if sentences > 0:
				message += ". "
			message += "It's good for your weight"
		if sentences == 0:
			message = "nothing special. Dish looks Ok for you"
		message = message.capitalize()
		return message

	@receiver(post_save, sender=User)
	def create_user_profile(sender, instance, created, **kwargs):
		if created:
			AppUser.objects.create(user=instance,email=instance.email)

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
	alt_name = products = models.TextField(null=True,blank=True,help_text='Enter list of alternative names for dish. Divider comma')
	eng_name = models.CharField(max_length=200,null=True)
	cooking_method = models.CharField(max_length=200,null=True)
	cousine = models.CharField(max_length=200,null=True)
	TYPE = models.CharField(max_length=200,null=True)
	tags = models.CharField(max_length=200,null=True,blank=True)
	products = models.TextField(null=True,blank=True,help_text="All words in lowercase and no spaces, use comma as a divider")
	weights = models.TextField(null=True,blank=True,help_text="Just numbers of weights of products in the same order as porducts, use comma as a divider")
	carbs = models.CharField(max_length=200,null=True,blank=True)
	fats = models.CharField(max_length=200,null=True,blank=True)
	proteins = models.CharField(max_length=200,null=True,blank=True)
	kcal = models.CharField(max_length=200,null=True,blank=True)
	comments = models.CharField(null=True,blank=True,max_length=200)
	avg_point = models.PositiveSmallIntegerField(default=30)
	frequency = models.CharField(max_length=200,default=30)
	specials_rules = models.CharField(max_length=200,null=True,blank=True)
	region = models.ForeignKey(Region,blank=True,null=True,on_delete=models.SET_NULL,db_index=False,default='russia')
	url = models.URLField(null=True,blank=True)
	parsed = models.BooleanField(default=False)

	def __str__(self):
		return self.name

class Product(models.Model):
	name = models.CharField(max_length=200, primary_key=True)
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
	weight_effect = models.SmallIntegerField(default=0)
	last_meal_date = models.DateField(auto_now=False,auto_now_add=False,null=True,blank=True)

	def __str__(self):
		string = "("
		string += str(self.user)
		string += ") "
		if self.dish:
			string += str(self.dish)
		elif self.product:
			string += str(self.product)
		else:
			string += "Unknown"
		return string

'''	@receiver(post_save, sender=Dish)
	def create_dish_preference_for_user(sender, instance, created, **kwargs):
		if created:
			users = AppUser.objects.all()
			for user in users:
				Preference.objects.create(TYPE='DS',user=user,dish=instance)

	@receiver(post_save, sender=Product)
	def create_product_preference_for_user(sender, instance, created, **kwargs):
		if created:
			users = AppUser.objects.all()
			for user in users:
				Preference.objects.create(TYPE='PR',user=user,product=instance)

	@receiver(post_save, sender=AppUser)
	def create_product_preference_for_user(sender, instance, created, **kwargs):
		if created:
			dishes = Dish.objects.all()
			for dish in dishes:
				Preference.objects.create(TYPE='DS',user=instance,dish=dish)
			products =Product.objects.all()
			for product in products:
				Preference.objects.create(TYPE='PR',user=instance,product=product)'''

def update_user_preference(user,dish,product,point,accepted):
	'''Here starts updating of user preferences'''
	dish_name = None
	if dish:
		try:
			dish_name = dish.name
			user_pref = Preference.objects.get(user=user,dish=dish_name)
		except Preference.DoesNotExist:
			user_pref = Preference.objects.create(TYPE='DS',user=user,dish=dish)
	else:
		try:
			user_pref = Preference.objects.get(user=user,product=product)
		except Preference.DoesNotExist:
			product_obj = Product.objects.get(name=product)
			user_pref = Preference.objects.create(TYPE='PR',user=user,product=product)
	preference = user_pref.preference
	preference = point_update(point,preference)
	if accepted:
		last_meal = user_pref.last_meal_date
		frequency = user_pref.frequency
		if last_meal:
			if datetime.date.today() < (last_meal + datetime.timedelta(days=5)):
				frequency += 1
			elif datetime.date.today() > (last_meal + datetime.timedelta(days=30)):
				frequency = 1
		else:
			frequency = 1
		new_last_meal = datetime.date.today()
		Preference.objects.filter(user=user,dish=dish_name,product=product).update(preference=preference,frequency=frequency,last_meal_date=new_last_meal)
	else:
		Preference.objects.filter(user=user,dish=dish_name,product=product).update(preference=preference)

class MealHistory(models.Model):
	date_time = models.DateTimeField(auto_now_add=True)
	dish = models.ForeignKey(Dish,null=True,blank=True,on_delete=models.SET_NULL,db_index=False) #dish id
	point = models.NullBooleanField()
	location = models.CharField(max_length=200,default='russia')
	user = models.ForeignKey(AppUser,null=True,blank=True,on_delete=models.SET_NULL,db_index=False) #user id
	weight = models.CharField(max_length=5,blank=True,null=True)
	acne = models.PositiveSmallIntegerField(blank=True,null=True)
	accepted = models.BooleanField(default=False)

	def save(self, *args, **kwargs):
		'''first scenario meal added
		that means program should take dish name and products and update their point and frequency'''
		if self.dish:
			#print(self.dish)
			dish = Dish.objects.filter(name=self.dish,region=self.location)[0]
			#print(dish)
			dish_point = dish.avg_point
			dish_products = dish.products
			dish_point = point_update(self.point,dish_point)
			dish.avg_point = dish_point
			dish.save()
			#print(self.accepted)
			update_user_preference(self.user,dish,None,self.point,self.accepted)
			try:
				products = dish_products.split(',')			
				for product in products:
					product_point = Product.objects.get(name=product)
					point = product_point.avg_point
					point = point_update(self.point,point)
					product_point.avg_point = point
					update_user_preference(self.user,None,product,self.point)
			except:
				#print('no products')
				pass
		'''first scenario weight added
		program should update user weight'''
		if (self.weight) and (self.accepted):
			AppUser.objects.filter(user=self.user.id).update(weigth=self.weight)
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

	def get_vector(self,region='russia'):
		self.dishes = self.calculate_location_vector_for(region=region)
		self.save()

	def __str__(self):
		self.date_time = str(self.date_time)[:19]
		return self.date_time
