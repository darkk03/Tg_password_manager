import sqlite3
from telebot import types
from authorization import check_password
from database import add_password as db_add_password
from database import get_passwords
from database import delete_password
import random
import string
import re

# Настройка команд для бота
def setup_commands(bot):
    # Обработчик команды /help
    @bot.message_handler(commands=['help'])
    def send_help(message):
        bot.reply_to(message, "Use command /start")

    # Обработчик команды /start
    @bot.message_handler(commands=['start'])
    def start(message):
        password = message.text.split()[-1]  
        if check_password(password):
            bot.send_message(message.chat.id, "Добро пожаловать! Вы авторизованы.")
            send_welcome(message)
        else:
            bot.send_message(message.chat.id, "Неверный пароль. Доступ запрещен.")

    # Отправка приветственного сообщения
    def send_welcome(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Add password") 
        item2 = types.KeyboardButton("Delete password")
        item3 = types.KeyboardButton("View passwords")
        item4 = types.KeyboardButton("Password generator")
        item5 = types.KeyboardButton("Verify passwords")
        item6 = types.KeyboardButton("Exit")

        markup.add(item1, item2, item3, item4, item5, item6)
        bot.send_message(message.chat.id, "Welcome to Telegram password-manager!", reply_markup=markup)





    #------------------------------------------------------------------------------------------------------------
    # Обработчик команды "Add password"

    @bot.message_handler(func=lambda message: message.text == "Add password")
    def add_password(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Add") 
        item2 = types.KeyboardButton("Back")  # Кнопка "Назад"

        markup.add(item1, item2)
        bot.send_message(message.chat.id, "Choose an option:", reply_markup=markup)

    # Обработчик команды "add"
    @bot.message_handler(func=lambda message: message.text == "Add")
    def option1(message):
        bot.send_message(message.chat.id, "Введите имя для пароля:")
        bot.register_next_step_handler(message, process_password_name)

    # Обработка имени пароля
    def process_password_name(message):
        password_name = message.text
        bot.send_message(message.chat.id, "Введите пароль:")
        bot.register_next_step_handler(message, process_password, password_name=password_name)


    # Обработка пароля
    def process_password(message, password_name):
        password = message.text
        db_add_password(password_name, password)  # Теперь передаем оба аргумента
        confirmation_message = f"Имя пароля: {password_name}\nПароль: {password}"
        bot.send_message(message.chat.id, confirmation_message)

    # Обработчик команды "Back"
    @bot.message_handler(func=lambda message: message.text == "Back")
    def back_to_menu(message):
        send_welcome(message)  # Возврат в меню

    #------------------------------------------------------------------------------------------------------------
    # Обработчик команды "Delete password"

    @bot.message_handler(func=lambda message: message.text == "Delete password")
    def delete_password_handler(message):
        try:
            passwords = get_passwords()
            if passwords:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item1 = types.KeyboardButton("Back")  # Кнопка "Назад"
                for name, _ in passwords:
                    markup.add(types.KeyboardButton(name))
                
                markup.add(item1)

                bot.send_message(message.chat.id, "Выберите пароль для удаления:", reply_markup=markup)
                bot.register_next_step_handler(message, process_password_name_for_deletion)  # Регистрируем обработчик
            else:
                bot.send_message(message.chat.id, "Пароли не найдены.")
        except sqlite3.ProgrammingError as e:
            bot.send_message(message.chat.id, f"Произошла ошибка при получении паролей: {str(e)}")

    def process_password_name_for_deletion(message):
        password_name = message.text
        if password_name == "Back":
            # Если пользователь нажал кнопку "Back", вернем его в меню
            return send_welcome(message)
        try:
            delete_password(password_name)
            bot.send_message(message.chat.id, f"Пароль '{password_name}' успешно удален.")
        except Exception as e:
            bot.send_message(message.chat.id, f"Произошла ошибка при удалении пароля: {str(e)}")
   
    #------------------------------------------------------------------------------------------------------------
    # Обработчик команды "View passwords"

    @bot.message_handler(func=lambda message: message.text == "View passwords")
    def view_passwords(message):
        try:
            passwords = get_passwords()
            if passwords:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
                item1 = types.KeyboardButton("Back")  # Кнопка "Назад"
                for name, _ in passwords:
                    markup.add(types.KeyboardButton(name))
                
                markup.add(item1)
                
                bot.send_message(message.chat.id, "Выберите пароль:", reply_markup=markup)
                bot.register_next_step_handler(message, show_selected_password)  # Регистрируем обработчик
            else:
                bot.send_message(message.chat.id, "Пароли не найдены.")
        except sqlite3.ProgrammingError as e:
            bot.send_message(message.chat.id, f"Произошла ошибка при получении паролей: {e}")

    # Обработчик для выбора пароля
    def show_selected_password(message):
        selected_password_name = message.text
        if selected_password_name == "Back":
            # Если пользователь нажал кнопку "Back", вернем его в меню
            return send_welcome(message)
        passwords = get_passwords()
        for name, password in passwords:
            if name == selected_password_name:
                bot.send_message(message.chat.id, f"Пароль: {password}")
                return
        
        bot.send_message(message.chat.id, "Пароль не найден.")


    #------------------------------------------------------------------------------------------------------------
    # password generator

    @bot.message_handler(func=lambda message: message.text == "Password generator")
    def generate(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("defolt") 
        item2 = types.KeyboardButton("custom")
        item3 = types.KeyboardButton("Back")

        markup.add(item1, item2, item3)
        bot.send_message(message.chat.id, "выбери:", reply_markup=markup)

        if generate == "Back":
            # Если пользователь нажал кнопку "Back", вернем его в меню
            return send_welcome(message)


    # Выбор функции дефолт
    @bot.message_handler(func=lambda message: message.text == "defolt")
    def generate_strong_password(message):
        password_length = 16  # Длина пароля
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for i in range(password_length))
        
        bot.send_message(message.chat.id, f"Сгенерированный надежный пароль:")
        bot.send_message(message.chat.id, password)


    # Выбор функции кастом и выбор длины пароля
    @bot.message_handler(func=lambda message: message.text == "custom")
    def generate_custom_password(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("8")
        item2 = types.KeyboardButton("12")
        item3 = types.KeyboardButton("16")
        item4 = types.KeyboardButton("20")
        markup.add(item1, item2, item3, item4)

        bot.send_message(message.chat.id, "выбери длину:", reply_markup=markup)
        bot.register_next_step_handler(message, choose_complexity)


    # Выбор сложности
    def choose_complexity(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Низкая")
        item2 = types.KeyboardButton("Средняя")
        item3 = types.KeyboardButton("Высокая")
        markup.add(item1, item2, item3)
        bot.send_message(message.chat.id, "выбери сложность:", reply_markup=markup)
        bot.register_next_step_handler(message, generate_custom_password_final, message.text)


    # скрещевание длины иложности + формирование пароля и вывод
    def generate_custom_password_final(message, password_length):

        password_length = int(password_length) 
        complexity = message.text
        if complexity == "Низкая":
            characters = string.ascii_letters
        elif complexity == "Средняя":
            characters = string.ascii_letters + string.digits
        else:
            characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for _ in range(password_length))
        bot.send_message(message.chat.id, f"Сгенерированный кастом пароль:")
        bot.send_message(message.chat.id, password)
        return send_welcome(message)


    #------------------------------------------------------------------------------------------------------------
    # password check


    # Функция для проверки надежности пароля
    

    @bot.message_handler(func=lambda message: message.text == "Verify passwords")
    def generate(message):
        try:
            passwords = get_passwords()
            if passwords:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
                item1 = types.KeyboardButton("Back")  # Кнопка "Назад"
                for name, _ in passwords:
                    markup.add(types.KeyboardButton(name))
                
                markup.add(item1)
                
                bot.send_message(message.chat.id, "Выберите пароль:", reply_markup=markup)
                bot.register_next_step_handler(message, check_selected_password)  # Регистрируем обработчик
        except sqlite3.ProgrammingError as e:
            bot.send_message(message.chat.id, f"Произошла ошибка при получении паролей: {e}")

    def check_selected_password(message):
        selected_password_name = message.text
        if selected_password_name == "Back":
            # Если пользователь нажал кнопку "Back", вернем его в меню
            return send_welcome(message)
        passwords = get_passwords()
        for name, password in passwords:
            if name == selected_password_name:
                result = check_password_strength(password)  # Проверяем надежность самого пароля, а не его имени
                bot.send_message(message.chat.id, result)  # Отправляем результат проверки обратно пользователю
                return
        
        bot.send_message(message.chat.id, "Пароль не найден.")



    def check_password_strength(password):
        # Проверяем длину пароля (минимум 8 символов)
        if len(password) < 8:
            return "Слабый пароль: слишком короткий"

        # Проверяем наличие букв верхнего и нижнего регистра
        if not any(c.isupper() for c in password) or not any(c.islower() for c in password):
            return "Слабый пароль: должны быть буквы верхнего и нижнего регистра"

        # Проверяем наличие цифр
        if not any(c.isdigit() for c in password):
            return "Слабый пароль: должны быть цифры"

        # Проверяем наличие специальных символов (например, !, @, #, $)
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return "Слабый пароль: должны быть специальные символы"

        return "Надежный пароль"



    