import sqlite3
import datetime

def get_time():
	timenow = datetime.datetime.now()
	timenow = timenow.strftime("%Y.%m.%d-%H:%M:%S")
	return timenow


class DBhelper:
	def __init__(self, dbname="all_dishes_list.db"):
		self.dbname = dbname
		self.conn = sqlite3.connect(dbname)
		self.cursor = self.conn.cursor()

	def get_uniq_values(self, column, from_table):
		uniq_values = []
		stmt = "SELECT DISTINCT {} FROM {}".format(column, from_table)
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
		values = []
		stmt = '''SELECT DISTINCT {} FROM {} WHERE {} = '{}' '''.format(column, from_table, with_column, equals)
		self.cursor.execute(stmt)
		value = self.cursor.fetchall()
		value = value[0][0]
		timenow = get_time()
		print(timenow, '{}:'.format(column), value)
		return value

	def insert_into_dishes(self, data):
		stmt = 'INSERT INTO Dishes VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'
		args = data
		print(data)
		try:
			self.cursor.execute(stmt,args)
			self.conn.commit()
		except sqlite3.IntegrityError:
			pass
		timenow = get_time()
		print(timenow, data[0], 'inserted')




