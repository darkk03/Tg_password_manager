from telebot import types
from authorization import check_password
from database import add_password
from database import add_password as db_add_password

def setup_commands(bot):
    @bot.message_handler(commands=['help'])
    def send_help(message):
        bot.reply_to(message, "Use command /start")

    @bot.message_handler(commands=['start'])
    def start(message):
        password = message.text.split()[-1]  # Получаем пароль из команды /start
        if check_password(password):
            bot.send_message(message.chat.id, "Добро пожаловать! Вы авторизованы.")
            send_welcome(message)
        else:
            bot.send_message(message.chat.id, "Неверный пароль. Доступ запрещен.")

    def send_welcome(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Add password") 
        item2 = types.KeyboardButton("Delete password")
        item3 = types.KeyboardButton("Show passwords")
        item4 = types.KeyboardButton("Strength password generator with AI")
        item5 = types.KeyboardButton("Verify password strength using AI")
        item6 = types.KeyboardButton("Exit")

        markup.add(item1, item2, item3, item4,item5, item6)
        bot.send_message(message.chat.id, "Welcome to Telegram password-manager!", reply_markup=markup)

    # Обработчик для команды "Add password"

    @bot.message_handler(func=lambda message: message.text == "Add password")
    def add_password(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Option 1") 
        item2 = types.KeyboardButton("Back")  # Кнопка "Назад"

        markup.add(item1, item2)
        bot.send_message(message.chat.id, "Choose an option:", reply_markup=markup)


    
    @bot.message_handler(func=lambda message: message.text == "Option 1")
    def option1(message):
        bot.send_message(message.chat.id, "Введите имя для пароля:")
        bot.register_next_step_handler(message, process_password_name)

    def process_password_name(message):
        password_name = message.text
        bot.send_message(message.chat.id, "Введите пароль:")
        bot.register_next_step_handler(message, process_password, password_name=password_name)


    def process_password(message, password_name):
        password = message.text
        db_add_password(password_name, password)  # Теперь передаем оба аргумента
        confirmation_message = f"Имя пароля: {password_name}\nПароль: {password}"
        bot.send_message(message.chat.id, confirmation_message)





