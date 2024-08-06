import sqlite3
from datetime import datetime


def create_tables():
    conn = sqlite3.connect('telgram_bot_data.db')
    c = conn.cursor()

    # Table to store user profiles
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (user_id INTEGER PRIMARY KEY, username TEXT, subscription_end DATE)''')

    conn.commit()
    conn.close()

def add_user(user_id, username):
    conn = sqlite3.connect('telgram_bot_data.db')
    c = conn.cursor()

    # Check if the user already exists in the database
    c.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    if c.fetchone() is None:
        # Add new user with a 7-day demo subscription
        from datetime import datetime, timedelta
        subscription_end = datetime.now() + timedelta(days=7)
        c.execute('INSERT INTO users (user_id, username, subscription_end) VALUES (?, ?, ?)',
                  (user_id, username, subscription_end.strftime('%Y-%m-%d')))

    conn.commit()
    conn.close()

def get_user_profile(user_id):
    conn = sqlite3.connect('telgram_bot_data.db')
    c = conn.cursor()
    c.execute('SELECT username, subscription_end FROM users WHERE user_id = ?', (user_id,))
    user = c.fetchone()
    conn.close()
    return user

def calculate_days_left(subscription_end):
    today = datetime.now().date()
    end_date = datetime.strptime(subscription_end, '%Y-%m-%d').date()
    days_left = (end_date - today).days
    return days_left
