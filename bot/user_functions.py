import sqlite3
from db_interface import Meal_history, User_list, Preference_tables
from vectors import Preference_vector

meal_history = Meal_history()
database = User_list()
preference = Preference_tables()

class User:
    #def __init__(self, chat):
    def auth(self, username):
        user_id = database.authorize(None,username)
        #print("success")
        if user_id:
            user_id = user_id[0]
        else:
            user_id = "New user"
        return user_id

    def create_an_account(self, name, telegram=None, region="russia", weight=None, growth=None, age=None):
        if telegram:
            user_id = database.add_new(name, region, telegram)
        else:   
            user_id = database.add_new(name, region, telegram=None)
        preference.setup(user_id)
        return user_id
        
    def about(self, user_id, name, weight, growth, age):
        self.name = name
        self.weight = weight
        self.growth = growth
        self.age = age
    
    def add_weight(self, user_id, weight):
        meal_history.add_weight(user_id, weight)

    def check_meal(self, user_id, meal_name):
        info = preference.get_dish_info(user_id, meal_name)
        meal_history.add_meal(user_id, meal_name)
        try:
            if float(info[1]) < 3.0 :
                pref_mess = "probably you would not like that dish"
                like = None
            elif float(info[1]) > 4.5:
                pref_mess = "that dish is on your taste"
                like = 1
            else:
                pref_mess = "it looks ok"
                like = None
            if int(info[2]) > 2:
                reit_mess = "you eat this dish too often"
            else:
                reit_mess = None
            if reit_mess and like:
                message = pref_mess.capitalize() + "but" + reit_mess
            elif like:
                message = pref_mess.capitalize() + ". Choose it"
            else:
                message = pref_mess.capitalize()
        except ValueError:
            message = info
        return message

    def accept_meal(self, user_id, meal, point=0):
        meal_name = meal[0]
        #print(meal_name)
        #print(point)
        meal_history.accept_meal(user_id, meal_name, point)

    def calculate_recommendations(self, user_id):
        preference_vector = Preference_vector(user_id)
        preference_vector.calc_prod_pref(user_id)
        preference_vector.calc_prior_prods(user_id)
        preference_vector.dishes_with_prod(user_id)
        preference_vector.calc_dish_pref(user_id)
        self.recommendations = preference_vector.calculate_vector(user_id)

def test():
    print()
    print("===")
    print("STARTING TEST")
    user = User()
    u_id = user.auth('berryrock')
    user.calculate_recommendations(u_id)
    x = user.recommendations
    return x
