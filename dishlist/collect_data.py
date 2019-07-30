from dbhelper import DBhelper


database = DBhelper()

'''Here is default dish data
First number is average dish point
Second number start frequency'''
default_data = [30, 10]

def formating(string):
	string = ','.join(string)
	print(string)
	return string

def cousine_tags_checking(dish,table_name):
	global cousine
	global tags
	data = database.get_filtered_one('dish_kitchen','dish_name',dish,table_name)
	if data:
		if 'кухня' in data:
			cousine = data.replace("кухня", "").format()
		else:
			tags = data

def collect_dish_info(dish,table_name,region='russia'):
	name = dish
	сousine = ""
	tags = ""
	cousine_tags_checking(dish, table_name)
	if tags == "":
		tags = database.get_filtered_one('dish_tag','dish_name',dish,table_name)
	TYPE = database.get_filtered_one('dish_type','dish_name',dish,table_name)
	products = database.get_filtered('dish_products_name','dish_name',dish,table_name)
	products = formating(products)
	carbs = database.get_filtered_one('dish_carbs','dish_name',dish,table_name)
	if carbs:
		carbs.replace(";", ",")
	fats = database.get_filtered_one('dish_fats','dish_name',dish,table_name)
	if fats:
		fats.replace(";", ",")
	proteins = database.get_filtered_one('dish_belki','dish_name',dish,table_name)
	if proteins:
		proteins.replace(";", ",")
	kcal = str(database.get_filtered_one('dish_kcal','dish_name',dish,table_name))
	if kcal:
		kcal.replace(";", ",")
	comments = database.get_filtered_one('dish_comments','dish_name',dish,table_name)
	avg_point = default_data[0]
	frequency = default_data[1]
	region_id = region
	special_rules = ''
	dish_info = [name, cousine, TYPE, tags, products, carbs, fats, proteins, kcal, comments, avg_point, frequency, special_rules, region_id]
	return dish_info