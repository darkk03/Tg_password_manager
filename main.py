from my_token import API_TOKEN
import telebot
from commands import setup_commands

bot = telebot.TeleBot(API_TOKEN)

if __name__ == '__main__':
    setup_commands(bot)
    bot.polling(non_stop=True)