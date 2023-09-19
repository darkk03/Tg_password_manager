
from telebot import types
from authorization import check_password

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
        item4 = types.KeyboardButton("Password generator")
        item5 = types.KeyboardButton("Exit")

        markup.add(item1, item2, item3, item4, item5)
        bot.send_message(message.chat.id, "Welcome to tgpassman!", reply_markup=markup)


