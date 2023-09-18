
from telebot import types

def setup_commands(bot):
    @bot.message_handler(commands=['help'])
    def send_help(message):
        bot.reply_to(message, "Use command /start")
    
    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Add password") 
        item2 = types.KeyboardButton("Delete password")
        item3 = types.KeyboardButton("Show passwords")

        markup.add(item1, item2, item3)
        bot.send_message(message.chat.id, "Welcome to tgpassman!", reply_markup = markup)

