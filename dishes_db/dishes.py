from dbhelper import DBhelper
import datetime


database = DBhelper()

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

def collect_dish_info(dish,table_name):
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
	fats = database.get_filtered_one('dish_fats','dish_name',dish,table_name)
	proteins = database.get_filtered_one('dish_belki','dish_name',dish,table_name)
	kcal = database.get_filtered_one('dish_kcal','dish_name',dish,table_name)
	dish_info = [name, cousine, TYPE, tags, products, carbs, fats, proteins, kcal]
	return dish_info

def main():
	new_table = input('Please, add name of the table with new recipes: ').strip()
	new_dishes = database.get_uniq_values('dish_name', new_table)
	print()
	print()
	for dish in new_dishes:
		dish_data = collect_dish_info(dish,new_table)
		database.insert_into_dishes(dish_data)
		print(dish, 'migrated')
		print()
		print()
	print('DONE')
	print()
	print()

if __name__ == '__main__':
	main()
