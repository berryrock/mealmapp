from dbhelper import DBhelper
import datetime

database = DBhelper()
default = '30'

def tpling(items):
	result = []
	for item in items:
		tpl = []
		tpl.append(item)
		tpl = tuple(tpl)
		result.append(tpl)
	result = tuple(result)
	return result

def make_product_list(LIST):
	items_list = []
	for items in LIST:
		item = items.split(",")
		items_list += item
	return items_list

def add_default(items):
	result = []
	for item in items:
		item = list(item)
		item.append(default)
		item = tuple(item)
		result.append(item)
	result = tuple(result)
	return result

def product_parsing():
	ingredients_list = database.get_filtered('products','parsed',0,'map_dish')
	dish_names = database.get_filtered('name','parsed',0,'map_dish')
	dish_names = tpling(dish_names)
	database.update('map_dish','parsed',1,'name',dish_names,'marked parsed')
	all_products = make_product_list(ingredients_list)

	#delete duplicates
	all_products = set(all_products)
	all_products = tpling(all_products)
	all_products = add_default(all_products)
	database.insert('map_product', 'name, avg_point', 2, all_products, 'added')
	print()
	print()
	print('DONE')
	print()
	print()


