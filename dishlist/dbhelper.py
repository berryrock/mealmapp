import sqlite3
import datetime
import os


def get_time():
	timenow = datetime.datetime.now()
	timenow = timenow.strftime("%Y.%m.%d-%H:%M:%S")
	return timenow

class DBhelper:
	def __init__(self, dbname='mealmapp.db'):
		db_dir = os.path.dirname(os.path.dirname(os.path.abspath('mealmapp.db')))
		self.dbname = dbname
		self.conn = sqlite3.connect(os.path.join(db_dir, dbname))
		self.cursor = self.conn.cursor()

	def get_uniq_values(self, column, from_table):
		uniq_values = []
		stmt = '''SELECT DISTINCT {} FROM '{}' '''.format(column, from_table)
		rows = self.cursor.execute(stmt)
		for row in self.cursor.fetchall():
			row = row[0]
			uniq_values.append(row)
		timenow = get_time()
		print(timenow, 'Unique {}:'.format(column), uniq_values)
		return uniq_values

	def get_values(self, column, from_table):
		result = []
		stmt = 'SELECT (?) FROM (?)'.format(column, from_table)
		self.cursor.execute(stmt)
		for row in self.cursor.fetchall():
			row = row[0]
			result.append(row)
		timenow = get_time()
		print(timenow, 'Results:',result)
		return result

	def get_filtered(self, column, with_column, equals, from_table):
		values = []
		stmt = '''SELECT {} FROM {} WHERE {} = '{}' '''.format(column, from_table, with_column, equals)
		self.cursor.execute(stmt)
		for row in self.cursor.fetchall():
			row = row[0]
			values.append(row)
		timenow = get_time()
		values = list(filter(None, values))
		print(timenow, '{}:'.format(column), values)
		return values

	def get_filtered_one(self, column, with_column, equals, from_table):
		value = 'Empty'
		stmt = '''SELECT DISTINCT {} FROM {} WHERE {} = '{}' '''.format(column, from_table, with_column, equals)
		try:
			self.cursor.execute(stmt)
			value = self.cursor.fetchall()
			value = value[0][0]
		except:
			pass
		timenow = get_time()
		print(timenow, '{}:'.format(column), value)
		return value

	def insert(self, into_table, column, vals_num, values, message=None):
		x = 1
		vals = '?'
		while x < vals_num:
			vals += ',?'
			x += 1
		stmt = '''INSERT INTO {}({}) VALUES ({})'''.format(into_table, column, vals)
		args = values
		self.cursor.executemany(stmt,args)
		self.conn.commit()
		timenow = get_time()
		print(timenow, values, message)

	def update(self, table, column, value, condition, equals, message):
		stmt = '''UPDATE {} SET {}={} WHERE {} = ?'''.format(table, column, value, condition)
		args = equals
		try:
			self.cursor.executemany(stmt,args)
			self.conn.commit()
		except sqlite3.IntegrityError:
			print("Integrity error")
		timenow = get_time()
		print(timenow, equals, message)


	def insert_into_dishes(self, data):
		stmt = 'INSERT INTO map_dish(name,cousine,TYPE,tags,products,carbs,fats,proteins,kcal,comments,avg_point,frequency,specials_rules,region_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
		args = data
		print(data)
		try:
			self.cursor.execute(stmt,args)
			self.conn.commit()
		except sqlite3.IntegrityError:
			print("Сouldn't add {} twice".format(data[0]))
		timenow = get_time()
		print(timenow, data[0], 'inserted')