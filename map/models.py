from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime


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
	dish = Preference.objects.get(dish=dish_data,user=user)
	point = dish.preference
	new_point = point_update(0,point)
	Preference.objects.filter(dish=dish_data).update(preference=new_point)

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

def calculate_user(user):
	print(timezone.now(), "/Starting user vector calculation/")
	prefered_dishes = []
	pref_products = Preference.objects.filter(user=user,TYPE='PR').order_by('-preference')[:20]
	all_dishes = Preference.objects.filter(user=user,TYPE='DS').order_by('-preference')
	for dish_preference in all_dishes:
		dish = Dish.objects.get(name=dish_preference.dish)
		num_pref_prod = 0
		for product_preference in pref_products:
			product = Product.objects.get(name=product_preference.product)
			num_pref_prod += check_entry(product,dish.products)
		if num_pref_prod > 1:
			prefered_dishes.append(dish.name)
	print(timezone.now(), prefered_dishes)
	return prefered_dishes


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
		region_vector = RegionVector.objects.order_by('-pk')[:1]
		prefered_dishes = calculate_user(self)
		'''dishes = region_vector.values_list("dishes", flat=True)[0]
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
										break'''
		print(prefered_dishes)
		n = 0
		for choosen_dish in prefered_dishes:
			n += 1
			lower_dish_points(choosen_dish,self)
			if n > 2:
				break
		result = {'id': self.id, 'vector': prefered_dishes}
		return result

	def get_dish_info(self, dish, user):
		#ALL VARIABLES LIST
		message = ""
		sentences = 0
		#PRODUCT VARIABLES
		products_preference_number = 30
		products_frequency_number = 30
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
		preference = Preference.objects.get(user=user,dish=dish)
		#print(preference)
		#print(preference.preference)
		try:
			product_list = dish.products
			products = product_list.split(',')
			for product in products:
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
				#PREFERENCES
				products_frequency.append(products_preferences[0])
				try:
					frequent_products.append(products_preferences[2])
				except:
					pass
			products_preference_number = calculate_avg_preference(products_preference)
			products_frequency_number = calculate_avg_preference(products_frequency)
		except:
			#print("No products")
			pass
		dish_preference = preference.preference
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
		dish_frequency = preference.frequency
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
	region = models.ForeignKey(Region,blank=True,null=True,on_delete=models.SET_NULL,db_index=False,default='russia')
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
	weight_effect = models.PositiveSmallIntegerField(default=30)
	last_meal_date = models.DateField(auto_now=False,auto_now_add=False,null=True,blank=True)

	def __str__(self):
		string = "("
		string += str(self.user)
		string += ") "
		if self.dish:
			string += str(self.dish)
		else:
			string += str(self.product)
		return string

	@receiver(post_save, sender=Dish)
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
				Preference.objects.create(TYPE='PR',user=instance,product=product)

def update_user_preference(user,dish,product,point,accepted):
	'''Here starts updating of user preferences'''
	#user = AppUser.objects.get(user=user)
	dish_name = None
	if dish:
		dish_name = dish.values_list('name',flat=True)[0]
		user_pref = Preference.objects.filter(user=user,dish=dish_name)
	else:
		user_pref = Preference.objects.filter(user=user,product=product)
	preference = user_pref.values_list('preference',flat=True)[0]
	preference = point_update(point,preference)
	if accepted:
		last_meal = user_pref.values_list('last_meal_date',flat=True)[0]
		frequency = user_pref.values_list('frequency',flat=True)[0]
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
			dish = Dish.objects.filter(name=self.dish,region=self.location)
			#print(dish)
			dish_point = dish.values_list("avg_point", flat=True)[0]
			dish_products = dish.values_list("products", flat=True)[0]
			dish_point = point_update(self.point,dish_point)
			Dish.objects.filter(name=self.dish).update(avg_point=dish_point)
			#print(self.accepted)
			update_user_preference(self.user,dish,None,self.point,self.accepted)
			try:
				products = dish_products.split(',')			
				for product in products:
					product_point = Product.objects.filter(name=product)
					point = product_point.values_list("avg_point", flat=True)[0]
					point = point_update(self.point,point)
					Product.objects.filter(name=product).update(avg_point=point)
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

	def __str__(self):
		self.date_time = str(self.date_time)[:19]
		return self.date_time
