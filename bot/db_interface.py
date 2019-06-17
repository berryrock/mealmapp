import sqlite3
import time

class DBhelper:
    def __init__(self, dbname="mealmapp.db"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)
        self.cursor = self.conn.cursor()

class Preference_tables(DBhelper):
    def setup(self, user_id):
        #create user product table
        product_table = """CREATE TABLE IF NOT EXISTS "{}_user_products" (name TEXT, point TEXT, last_update INTEGER, repeating INTEGER, preference TEXT)""".format(user_id)
        self.cursor.execute(product_table)
        self.conn.commit()
        copy_default_table = """INSERT INTO "{}_user_products" SELECT * FROM default_user_products""".format(user_id)
        self.cursor.execute(copy_default_table)
        self.conn.commit()
        #create user dishes table
        dish_table = """CREATE TABLE IF NOT EXISTS "{}_user_dishes" (name TEXT, point TEXT, last_update INTEGER, repeating INTEGER, preference TEXT)""".format(user_id)
        self.cursor.execute(dish_table)
        self.conn.commit()
        copy_default_table = """INSERT INTO "{}_user_dishes" SELECT * FROM default_user_dishes""".format(user_id)
        self.cursor.execute(copy_default_table)
        self.conn.commit()
        #create preference vector
        user_pref_vector = """ALTER TABLE "preference_vector" ADD COLUMN "{}" TEXT""".format(user_id)
        self.cursor.execute(user_pref_vector)
        self.conn.commit()

    def get_dish_info(self, user_id, dish_name):
        stmt1 = 'SELECT point FROM "{}_user_dishes" WHERE name = (?)'.format(user_id)
        self.cursor.execute(stmt1, (dish_name,))
        self.conn.commit()
        dish_point = self.cursor.fetchone()
        stmt2 = 'SELECT repeating FROM "{}_user_dishes" WHERE name = (?)'.format(user_id)
        self.cursor.execute(stmt2, (dish_name,))
        self.conn.commit()
        dish_repeating = self.cursor.fetchone()
        dish_info = []
        if dish_point and dish_repeating:
            dish_info.append(dish_name)
            dish_info.append(dish_point[0])
            dish_info.append(dish_repeating[0])
        else:
            dish_info = "No information about dish. We will add it later"
            self.cursor.execute('INSERT INTO "new_dishes" (name) VALUES (?)', (dish_name,))
            self.conn.commit()
        #print(dish_info)
        return dish_info

    def all_dishes(self):
        stmt = "SELECT * FROM all_dishes_list"
        self.cursor.execute(stmt)
        dishes = self.cursor.fetchall()
        return dishes

    #USER PREFERENCE FUNCTIONS
    def user_pref(self, user_id, table_name):
        stmt = 'SELECT * FROM "{}_user_{}"'.format(user_id, table_name)
        self.cursor.execute(stmt)
        items = self.cursor.fetchall()
        #print(items)
        return items

    def user_pref_dishes(self, user_id, dish):
        stmt = 'SELECT * FROM "{}_user_dishes" WHERE name = (?)'.format(user_id)
        self.cursor.execute(stmt, (dish,))
        return [x for x in self.cursor.fetchone()]

    def upload_pref(self, user_id, item, table_name):
        upload_preference = 'UPDATE "{}_user_{}" SET point = (?), last_update = (?), repeating = (?), preference = (?)  WHERE name = (?)'.format(user_id, table_name)
        self.cursor.executemany(upload_preference, (item,))
        self.conn.commit()

    def clear_pref(self, user_id, table_name):
        stmt = 'UPDATE "{}_user_{}" SET preference = 1'.format(user_id, table_name)
        self.cursor.execute(stmt)
        self.conn.commit()

    def prior_prod(self, user_id):
        stmt = 'SELECT name FROM "{}_user_products" ORDER BY preference DESC'.format(user_id)
        self.cursor.execute(stmt)
        products = self.cursor.fetchall()
        return products

    def vector(self, user_id):
        stmt = 'SELECT name FROM "{}_user_dishes" ORDER BY preference DESC'.format(user_id)
        self.cursor.execute(stmt)
        vector = sum(self.cursor.fetchall(),())
        self.conn.commit()
        return vector

    #USER PREFERENCE FUNCTIONS

class User_list(DBhelper):
    def setup(self):
        tblstmt = "CREATE TABLE IF NOT EXISTS user_list (id INTEGER, user_name TEXT, height INTEGER, age INTEGER, region TEXT, telegram TEXT)"
        itemidx = "CREATE INDEX IF NOT EXISTS userIndex ON user_list (id ASC)"
        tgmidx = "CREATE INDEX IF NOT EXISTS tgmIndex ON user_list (telegram ASC)"
        self.conn.execute(tblstmt)
        self.conn.execute(itemidx)
        self.conn.execute(tgmidx)
        self.conn.commit()

    def add_new(self, name, region="russia", telegram=None):
        #get new id
        [max_id], = self.conn.execute("SELECT MAX(user_id) FROM user_list")
        print(max_id)
        user_id = max_id +1
        insert_user = """INSERT INTO "user_list" (user_id, user_name, region, telegram) VALUES (?,?,?,?)"""
        args = (user_id, name, region, telegram)
        self.cursor.execute(insert_user, args)
        self.conn.commit()
        #preference_tables.setup(user_id)
        #self.conn.commit()
        return user_id

    def add_growth(self, user_id, growth):
        #get new id
        self.conn.execute("SELECT MAX(user_id) FROM user_list")
        user_id = [x[0] for x in self.cursor.fetchone()]
        user_id += 1
        insert_user = """INSERT INTO "user_list" VALUES (?,?,?,?,?,?)"""
        args = (name, weight, growth, age, region, telegram)
        cursor.execute(insert_user, args)
        conn.commit()
        preference_tables.setup(user_id)
        conn.commit()
        
    def authorize(self, name=None, telegram=None):
        if telegram:
            telegram = str(telegram)
            stmt = 'SELECT user_id FROM user_list WHERE telegram = ?'
            args = (telegram,)
        else:
            stmt = "SELECT user_id FROM user_list WHERE user_name = (?)"
            args = (name, )
        self.cursor.execute(stmt, args)
        user_id = self.cursor.fetchone()
        self.conn.commit()
        #print(user_id)
        return user_id

class Meal_history(DBhelper):
    def setup(self):
        tblstmt = "CREATE TABLE IF NOT EXISTS meal_history (date TEXT, user_id INTEGER, meal_name TEXT, time TEXT, point INT, weight TEXT)"
        dateidx = "CREATE INDEX IF NOT EXISTS dateIndex ON meal_history (date ASC)"
        useridx = "CREATE INDEX IF NOT EXISTS userIndex ON meal_history (user_id ASC)"
        self.conn.execute(tblstmt)
        self.conn.execute(dateidx)
        self.conn.execute(useridx)
        self.conn.commit()

    def add_meal(self, user_id, meal_name):
        stmt = "INSERT INTO meal_history (date, user_id, meal_name, time,  status) VALUES (?, ?, ?, ?, ?)"
        date = "test"
        time = "test"
        point = 0
        status = "check"
        args = (date, user_id, meal_name, time, status)
        try:
            self.conn.execute(stmt, args)
            print(user_id, meal_name)
            self.conn.commit()
        except sqlite3.IntegrityError:
            print("Error in adding meal")

    def accept_meal(self, user_id, meal_name, point):
        date = "test"
        status = "accept"
        data = (meal_name, user_id, date)
        args = []
        args.append(status)
        args.append(point)
        stmt = 'UPDATE meal_history SET status = (?) AND point = (?) WHERE meal_name = "{}" AND user_id = {} AND date = "{}"'.format(*data)
        try:
            self.conn.executemany(stmt, (args,))
            print(user_id, meal_name)
            self.conn.commit()
        except sqlite3.IntegrityError:
            print("Error in accepting meal")

    def delete_meal(self, user_id, meal_name,):
        stmt = "DELETE FROM meal_history WHERE user_id = (?) AND meal_name = (?)"
        args = (user_id, meal_name)
        try:
            self.conn.execute(stmt, args)
            self.conn.commit()
        except sqlite3.IntegrityError:
            print("Error in deleting meal")

    def add_weight(self, user_id, weight):
        stmt = "UPDATE meal_history SET weight = (?) WHERE user_id = (?) AND date = (?)"
        date = "test"
        args = (weight, user_id, date)
        #print(args)
        try:
            self.conn.execute(stmt, args)
            self.conn.commit()
        except sqlite3.IntegrityError:
            print("Error in adding weight")
        
    def get_meals(self, user_id):
        stmt = "SELECT meal_name AND date FROM meal_history WHERE user_id = (?)"
        args = (user_id, )
        return [x[0] for x in self.conn.execute(stmt, args)]
