import sqlite3

def add_password_to_db(password_name, password_value):
    conn = sqlite3.connect('pass.db')
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO passwordman (password_name, password_value) VALUES (?, ?)",
                   (password_name, password_value))
    
    conn.commit()
    conn.close()
