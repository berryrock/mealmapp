import json
import requests
import time
import urllib
from user_functions import User
from db_interface import User_list

access = User_list()
step_weight = []
step_meal = []
user_choice = {}

token = "824907378:AAHvvoezizNc3rvBuugigsUvkBhLlFMg5_k"
URL = "https://api.telegram.org/bot{}/".format(token)

main_menu = ("/recommedations", "/meal", "/add_weight")

#REQUEST STRUCTURE
def get_request_to(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content

def get_json_from(url):
    content = get_request_to(url)
    answer = json.loads(content)
    return answer

#API methods
def get_me():
    url = URL + "getme"
    answer = get_json_from(url)
    return answer

def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    answer = get_json_from(url)
    return answer 

def send_message(text, chat_id, reply_markup=None):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text,chat_id)
    if reply_markup:
        url += "&reply_markup={}".format(reply_markup)
    #print(url)
    get_request_to(url) 

def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)

def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    #print(text)
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    #print(chat_id)
    return (text, chat_id)

def add_a_keyboard(items):
    keyboard = [[item] for item in items]
    reply_markup = {"keyboard":keyboard, "one_time_keyboard":True}
    return json.dumps(reply_markup)

#//REQUEST STRUCTURE

#FUNCTIONS
def clear_meal_history(user_id):
    try:
        del user_choice[user_id]
    except KeyError:
        pass

def check_command(updates):
    step = None
    x = updates["result"]
    update = x[0]
    #print("UPDATE")
    #print(update)
    text = update["message"]["text"]
    chat = update["message"]["chat"]["id"]  
    if text == "/add_weight":
        step = "add_weight"
    else:
        pass
    return step

def check_step(user_id):
    if user_id in step_meal:
        step = "check_meal"
    elif user_id in step_weight:
        step = "add_weight"
    else:
        step = None
    return step

def go_on_step(step, user, user_id, text, chat):
    if step == "check_meal":
        dish_name = text.lower()
        user_meal = {}
        message = user.check_meal(user_id, dish_name)
        for_meal = ("/add_it", "/try_another", "/main_menu")
        keyboard = add_a_keyboard(for_meal)
        info = """Dish name: {}

Comments:
{}
""".format(dish_name, message)
        send_message(info, chat, keyboard)
        step_meal.remove(user_id)
        point = 0
        added_meal = {user_id: [dish_name, point]}
        user_choice.update(added_meal)
        #print(user_choice)
    elif step == "add_weight":
        user.add_weight(user_id, text)
        keyboard = add_a_keyboard(main_menu)
        send_message("Weight added. Main menu", chat, keyboard)
        step_weight.remove(user_id)
    else:
        keyboard = add_a_keyboard(main_menu)
        send_message("From unknown step to main menu", chat, keyboard)

def follow_command(user, user_id, text, chat):
    if text == "/main_menu":
        keyboard = add_a_keyboard(main_menu)
        send_message("Main menu", chat, keyboard)
    elif text == "/recommedations":
        user.calculate_recommendations(user_id)
        full_recommendations = user.recommendations
        print(full_recommendations)
        recommendations = full_recommendations[:3]
        keyboard = add_a_keyboard(recommendations)
        send_message("Recommended for you", chat, keyboard)
        step_meal.append(user_id)
    elif text == "/meal" or text == "/try_another":
        for_meal = ("/main_menu",)
        keyboard = add_a_keyboard(for_meal)
        send_message("Enter dish name to check or add it", chat, keyboard)
        step_meal.append(user_id)
    elif text == "/add_weight":
        for_weight = ("/main_menu",)
        keyboard = add_a_keyboard(for_weight)
        send_message("Enter your weight", chat, keyboard)
        step_weight.append(user_id)
    elif text == "/start":
        send_message("Mealmapp - your personal nutrition assistant", chat)
    elif text == "/add_it":
        user.accept_meal(user_id, user_choice[user_id])
        keyboard = add_a_keyboard(main_menu)
        send_message("Meal added. Main menu", chat, keyboard)
        clear_meal_history(user_id)
    elif text.startswith("/"):
        pass
    else:
        keyboard = add_a_keyboard(main_menu)
        send_message("Main menu", chat, keyboard)  

def handle_updates(updates):
    for update in updates["result"]:
        step = None
        #print(user_choice)
        try:
            text = update["message"]["text"]
            chat = update["message"]["chat"]["id"]
            username = update["message"]["from"]["username"]
            user = User()
            user_id = user.auth(username)
            print("auth:", user_id)
            if user_id != "New user":
                step = check_step(user_id)
            else:
                user_id = user.create_an_account(username, username)
            if step:
                clear_meal_history(user_id)
                go_on_step(step, user, user_id, text, chat)
            else:
                follow_command(user, user_id, text, chat)
            #print(user_id)
        except KeyError:
            print("Key Error in Updates")
#//FUNCTIONS

#FLOW

#text, chat = get_last_chat_id_and_text(get_updates())
#send_message(text,chat)

def main():
    #database.setup()
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            handle_updates(updates)
        time.sleep(0.5)

if __name__ == '__main__':
    main()
    
#//FLOW
