from dbhelper import DBhelper
import datetime
from collect_data import collect_dish_info


database = DBhelper()

def dishes_migration():
	new_table = input('Please, add name of the table with new recipes: ').strip()
	region = input('For region(enter id): ').strip()
	new_dishes = database.get_uniq_values('title', new_table)
	print()
	print()
	for dish in new_dishes:
		dish_data = collect_dish_info(dish,new_table,region)
		database.insert_into_dishes(dish_data)
		print(dish, 'migrated...')
		print()
		print()
	print('DONE')
	print()
	print()
