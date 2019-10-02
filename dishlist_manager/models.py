from django.db import models
from django.utils import timezone
from map.models import Dish, Product
from django.db import IntegrityError
import csv
from io import StringIO

# Create your models here.

def check_headings(row):
	print(row)
	items_positions = {}
	n = 0
	for item in row:
		items_positions.update({item: n})
		n += 1
	print(items_positions)
	return items_positions

def parse_dish_to(items):
	number_of_created_items = 0
	items_list = items.split(',')
	for item in items_list:
		try:
			Product.objects.create(name=item)
			print('Created', item)
			number_of_created_items += 1
		except IntegrityError:
			print(item, 'already exist in database')
	return number_of_created_items



class DishList(models.Model):
	name = models.CharField(max_length=200)
	file = models.FileField(upload_to='uploads/')

	def __str__(self):
		return self.name

	def get_dishes_from_csv(self):
		file = self.file.read().decode('utf-8')
		csv_data = csv.reader(StringIO(file), delimiter=',')
		n = 0
		number_of_dishes = 0
		number_of_duplicates = 0
		number_of_products = 0
		for row in csv_data:
			print()
			n += 1
			if n == 1:
				positions = check_headings(row)
			else:
				print(row)
				name = None
				alt_name = None
				eng_name = None
				cooking_method = None
				kitchen = None
				TYPE = None
				tags = None
				products = None
				weights = None
				carbs = None
				fats = None
				proteins = None
				kcal = None
				comments = None
				url = None

				name = positions.get('title', None)
				if name:
					name = row[name]

				alt_name = positions.get('alt_name', None)
				if alt_name:
					alt_name = row[alt_name]

				eng_name = positions.get('eng_name', None)
				if eng_name:
					eng_name = row[eng_name]

				cooking_method = positions.get('cooking_method', None)
				if cooking_method:
					cooking_method = row[cooking_method]

				cousine = positions.get('kitchen', None)
				if cousine:
					cousine = row[cousine]

				TYPE = positions.get('type', None)
				if TYPE:
					TYPE = row[TYPE]

				tags = positions.get('tags', None)
				if tags:
					tags = row[tags]

				products = positions.get('products', None)
				if products:
					products = row[products]

				weights = positions.get('weights', None)
				if weights:
					weights = row[weights]

				carbs = positions.get('carbs', None)
				if carbs:
					carbs = row[carbs]

				fats = positions.get('fats', None)
				if fats:
					fats = row[fats]

				proteins = positions.get('proteins', None)
				if proteins:
					proteins = row[proteins]

				kcal = positions.get('kcal', None)
				if kcal:
					kcal = row[kcal]

				comments = positions.get('comments', None)
				if comments:
					comments = row[comments]

				url = positions.get('url', None)
				if url:
					url = row[url]

				try:
					Dish.objects.create(name=name.capitalize(),
						alt_name=alt_name,
						eng_name=eng_name,
						cooking_method=cooking_method,
						cousine=cousine,
						TYPE=TYPE,
						tags=tags,
						products=products,
						weights=weights,
						carbs=carbs,
						fats=fats,
						proteins=proteins,
						kcal=kcal,
						comments=comments,
						url=url)
					print('Created', name)
					number_of_dishes += 1
					created_products = parse_dish_to(products)
					number_of_products += created_products
					if created_products > 0:
						parsed = True
					else:
						parsed = False
					Dish.objects.filter(name=name).update(parsed=parsed)
				except IntegrityError:
					print(name, 'already exist in database')
					number_of_duplicates += 1
				except AttributeError:
					print('''Dish can't be created without NAME''')
		print()
		print(number_of_dishes, 'new dishes have created')
		print(number_of_products, 'new products have created')
		print(number_of_duplicates, 'dishes were duplicates')

		