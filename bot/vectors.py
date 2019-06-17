from db_interface import Preference_tables

preference = Preference_tables()

#recomendation functions
def calculate_reiteration(last_update_day,reiteration):
    #print(last_update_day)
    if int(last_update_day) < 3:
        reiteration += 1
    elif int(last_update_day) > 29:
        reiteration = 1
    else:
        pass
    return reiteration

def calculate_preference(point,reiteration):
    preference = float(point) / float(reiteration)
    return preference

class Preference_vector():
    def __init__(self, user_id):
        print("Vector of preference for", user_id)

    def calc_prod_pref(self, user_id):
        #calculate prefered products. import table of products
        preference.clear_pref(user_id, "products")
        products = preference.user_pref(user_id, "products")
        for product in products:
            product = list(product)
            #print(product)
            product[3] = calculate_reiteration(product[2], product[3])
            product[4] = calculate_preference(product[1], product[3])
            #upload new preference
            updated_product = [product[1],product[2],product[3],product[4],product[0]]
            preference.upload_pref(user_id, updated_product, "products")
            #print(updated_product)

    def calc_prior_prods(self, user_id):
        #20 times for 20 first products
        number_prefered_products = 0
        self.prefered_products = []
        products = preference.prior_prod(user_id)
        for product in products:
            number_prefered_products += 1
            product = product[0]
            self.prefered_products.append(product)
            if number_prefered_products == 20:
                break
            else:
                pass
        #print('===CHECKING===', self.prefered_products)

    def dishes_with_prod(self, user_id):
        #calculate dishes which include prefered products. import table of dishes
        self.dishes_with_prod = []
        dishes = preference.all_dishes()
        for dish in dishes:
            #print(dish)
            products = dish[4].split(',')
            #print(products)
            number_of_prefered_products_in_dish = 0
            for product in products:
                #print(product)
                if any(product in s for s in self.prefered_products):
                    number_of_prefered_products_in_dish += 1
                    #print(number_of_prefered_products_in_dish, 'for', dish[0])
                else:
                    pass
            if number_of_prefered_products_in_dish > 1:
                self.dishes_with_prod.append(dish[0])
            else:
                pass
        #print('===CHECKING===', self.dishes_with_prod)

    def calc_dish_pref(self, user_id):
        #calculate prefered dishes. import table of dishes
        preference.clear_pref(user_id, "dishes")
        for dish in self.dishes_with_prod:
            pref_dish = preference.user_pref_dishes(user_id,dish)
            pref_dish[3] = calculate_reiteration(pref_dish[2],pref_dish[3])
            pref_dish[4] = calculate_preference(pref_dish[1],pref_dish[3])
            #print(pref_dish)
            #upload new preference
            updated_dish = [pref_dish[1],pref_dish[2],pref_dish[3],pref_dish[4],pref_dish[0]]
            preference.upload_pref(user_id, updated_dish, "dishes")
        
    def calculate_vector(self, user_id):
        preference_vector = preference.vector(user_id)
        #print(preference_vector)
        recommendations = preference_vector[:8]
        #print(recommendations)
        return recommendations
