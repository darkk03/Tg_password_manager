import sqlite3

# Создаем базу данных или подключаемся к существующей
conn = sqlite3.connect('passwords.db')
cursor = conn.cursor()

# Создаем таблицу для хранения паролей
cursor.execute('''
    CREATE TABLE IF NOT EXISTS passwords (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        password TEXT NOT NULL
    )
''')

def create_table():
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_password(name, password):
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    create_table()
    cursor.execute('INSERT INTO passwords (name, password) VALUES (?, ?)', (name, password))
    conn.commit()
    conn.close()

def delete_password(name):
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM passwords WHERE name = ?', (name,))
    conn.commit()
    conn.close()


# Функция для получения списка всех паролей из базы данных
def get_passwords():
    cursor.execute('SELECT name, password FROM passwords')
    return cursor.fetchall()

# Закрываем соединение с базой данных при выходе из программы
def close_database():
    conn.close()