from map.models import RegionVector, Dish, Product, MealHistory
#from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from django.utils import timezone

'''
def update_product_avg_point():
	print(timezone.now(), "/Updating avg product points/")
	last_hour_meals = MealHistory.objects.filter(date_time__gte=timezone.now()+timezone.timedelta(hours=1))
	for meal in last_hour_meals:
		dish = Dish.objects.get(name=meal.dish)
		products = dish.products
		for product in products:
			if meal.point == True:
				product.avg_point += 2
			elif meal.point == False:
				product.avg_point -= 2
			else:
				product.avg_point += 1
			product.save()
'''

'''
def update_dish_avg_point():
	print(timezone.now(), "/Updating avg dish points/")
	last_hour_meals = MealHistory.objects.filter(date_time__gte=timezone.now()+timezone.timedelta(hours=1))
	for meal in last_hour_meals:
		dish = Dish.objects.get(name=meal.dish)
		if meal.point == True:
			dish.avg_point += 2
		elif meal.point == False:
			dish.avg_point -= 2
		else:
			dish.avg_point += 1
		dish.save()
'''

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

def calculate_region():
	print(timezone.now(), "/Starting vector calculation/")
	prefered_dishes = []
	pref_products = Product.objects.order_by('-avg_point')[:20]
	all_dishes = Dish.objects.order_by('-avg_point')
	for dish in all_dishes:
		num_pref_prod = 0
		for product in pref_products:
			num_pref_prod += check_entry(product,dish.products)
		if num_pref_prod > 1:
			prefered_dishes.append(dish.name)
	new_vector = RegionVector()
	new_vector.dishes = prefered_dishes
	new_vector.save(prefered_dishes)
	print(timezone.now(), prefered_dishes)

def calculate_user():
	print(timezone.now(), "/Starting user vector calculation/")
	prefered_dishes = []

