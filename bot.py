from logic import DB_Manager
from config import *
from telebot import TeleBot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telebot import types

bot = TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start_command(message):
    bot.send_message(message.chat.id, """Привет! Я бот-поваренок (only eng)\n
мои команды:
/random3 отправляет 3 рецептa
/random10- отправляет 10 рецептов
/random5- отправляет 5 рецептов
/info (название блюда) - расказывает рецепт и как готовить блюдо
/ingredient (название Ингридиентa(на англ.) - введите ингредиент и получи 15 блюд с ним
/add_recipe добавьте свой рецепт
/add_favorite (рецепт)-добавляет в избранное рецепт
/my_favorites - показывает избранные рецепты ) """)



@bot.message_handler(commands=['random3'])
def start_command(message):
    ran3 =  manager.get_random_recipe_3()
    ran3_text = "\n".join([recipe[0] for recipe in ran3])  # Преобразуем список рецептов в строку
    bot.send_message(message.chat.id, f"Вот ваши 3 рецепта:\n{ran3_text}")


@bot.message_handler(commands=['random5'])
def random5_command(message):
    ran5 = manager.get_random_recipe_5()
    ran5_message = "\n".join([recipe[0] for recipe in ran5])  # Формируем строку из названий рецептов
    bot.send_message(message.chat.id, f"Вот ваши 5 рецептов:\n{ran5_message}")

@bot.message_handler(commands=['random10'])
def random10_command(message):
    ran10 = manager.get_random_recipe_10()
    ran10_message = "\n".join([recipe[0] for recipe in ran10])  # Формируем строку из названий рецептов
    bot.send_message(message.chat.id, f"Вот ваши 10 рецептов:\n{ran10_message}")

@bot.message_handler(commands=['info'])
def info(message):
    name = " ".join(message.text.split()[1:])
    info = manager.get_info_recipe(name)
    if info:
        response = ''
        for rec in info:
            recipe_name, minutes, n_steps, steps, ingredients = rec
            response += f"🍽 Название: {recipe_name}\n"
            response += f"⏱ Время: {minutes} минут\n"
            response += f"📋 Шагов: {n_steps}\n"
            response += f"🧾 Ингредиенты: {ingredients}\n"
            response += f"🔪 Шаги: {steps}\n"
        bot.send_message(message.chat.id, response)
    else:
        bot.send_message(message.chat.id, f"Рецепт '{name}' не найден ")



@bot.message_handler(commands=['ingredient'])
def ingredient(message):
    name = " ".join(message.text.split()[1:])
    if name:
        ingr = manager.find_by_ingredient(name)
        ingridient = "\n".join([recipe[0] for recipe in ingr])
        bot.send_message(message.chat.id, f"Вот 15 рецептов по вашему запросу {name}:\n{ingridient}")
    else:
        bot.send_message(message.chat.id, f"Ингридиент '{name}' не найден ")




@bot.message_handler(commands=['add_favorite'])
def add_favorite(message):
    name = " ".join(message.text.split()[1:])
    user_id = message.from_user.id
    add = manager.add_favorite(user_id, name)
    if add:
        bot.send_message(message.chat.id, f"Рецепт '{name}' добавлен в избраное")
    else:
        bot.send_message(message.chat.id, "Erorr") 




@bot.message_handler(commands=['my_favorites'])
def myfavorites_command(message):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Посмотреть избранное", callback_data="show_favorites"))
    bot.send_message(message.chat.id, "Нажми на кнопку, чтобы увидеть свои любимые рецепты 👇", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "show_favorites")
def show_favorites_callback(call):
    user_id = call.from_user.id
    favorites = manager.get_favorites(user_id)
    if not favorites:
        bot.send_message(call.message.chat.id, 'У тебя нету избраных, добавь с помощью команды /add_favorite (рецепт)')
    else:
        markup = InlineKeyboardMarkup()
        for (name,) in favorites:
            markup.add(InlineKeyboardButton(text=name, callback_data=f"fav_{name}"))
        bot.send_message(call.message.chat.id, "Вот твои избранные рецепты👇", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("fav_"))
def info(call):
    name = call.data[4:]
    info = manager.get_info_recipe(name)
    if info:
        response = ''
        for rec in info:
            recipe_name, minutes, n_steps, steps, ingredients = rec
            response += f"🍽 Название: {recipe_name}\n"
            response += f"⏱ Время: {minutes} минут\n"
            response += f"📋 Шагов: {n_steps}\n"
            response += f"🧾 Ингредиенты: {ingredients}\n"
            response += f"🔪 Шаги: {steps}\n"
        bot.send_message(call.message.chat.id, response)
    else:
        bot.send_message(call.message.chat.id, f"Рецепт '{name}' не найден ")






@bot.message_handler(commands=['add_recipe'])
def add(message):
    bot.send_message(message.chat.id, "Введите название (старайтесь все писать на английском (по возможности)) :")
    bot.register_next_step_handler(message, name_recipe)

def name_recipe(message):
    name = message.text
    data = [name]
    bot.send_message(message.chat.id, "Введите время приготовления")
    bot.register_next_step_handler(message, minutes , data=data)

def minutes(message, data):
    minutes = message.text
    data.append(minutes)
    bot.send_message(message.chat.id, "Введите сегодняшнюю дату ")
    bot.register_next_step_handler(message, date, data=data)  

def date(message, data):
    date = message.text
    data.append(date)
    bot.send_message(message.chat.id, "Введите теги(по типу горячее, холодное) ")
    bot.register_next_step_handler(message, tags, data=data)  

def tags(message, data):
    tags = message.text
    data.append(tags)
    bot.send_message(message.chat.id, "Введите этапы приготовления(после каждого этапа ставьте запятую) ")
    bot.register_next_step_handler(message, steps, data=data)  

def steps(message, data):
    steps = message.text
    data.append(steps)
    bot.send_message(message.chat.id, "Введите описание ")
    bot.register_next_step_handler(message, description, data=data)  

def description(message, data):
    description = message.text
    data.append(description)
    bot.send_message(message.chat.id, "Введите ингридиенты(после каждого ингридиента ставьте запятую) ")
    bot.register_next_step_handler(message, ingredients, data=data) 

def ingredients(message, data):
    ingredients = message.text
    user_id = message.from_user.id
    data.insert(2, user_id)
    data.append(ingredients)
    manager.add_recipe([tuple(data)])
    bot.send_message(message.chat.id, " ✅успешно добавлено")        





if __name__ == '__main__':
    manager = DB_Manager(DATABASE)
    bot.infinity_polling()