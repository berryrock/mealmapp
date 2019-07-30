from dbhelper import DBhelper
from dishes_migration import dishes_migration
from product_parsing import product_parsing


database = DBhelper()

def main():
	while True:
		print('''Available commands:
		1. Dishes migration
		2. Product parsing''')
		print()
		command = input('Enter command: ').lower()
		if command == '1' or command == 'dishes migration':
			dishes_migration()
		elif command == '2' or command == 'product parsing':
			product_parsing()
		else:
			print('Wrong command. Try again')


if __name__ == '__main__':
	main()