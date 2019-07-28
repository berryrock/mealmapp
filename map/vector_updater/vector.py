from map.models import RegionVector, Dish, Product, MealHistory
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from django.utils import timezone

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

def calculate_region():
	print(timezone.now(), "/Starting vector calculation/")
	prefered_dishes = []
	update_product_avg_point()
	update_dish_avg_point()
	pref_products = Product.objects.order_by('avg_point')[:20]
	all_dishes = Dish.objects.order_by('avg_point')
	for dish in all_dishes:
		num_pref_prod = 0
		for product in pref_products:
			if product in dish.products:
				num_pref_prod += 1 
			else:
				pass
		if num_pref_prod > 1:
			prefered_dishes.append(dish.name)
	try:
		new_vector = RegionVector()
		new_vector.dishes = prefered_dishes
		print(timezone.now(), prefered_dishes)
	except:
		print(timezone.now(), 'error')
