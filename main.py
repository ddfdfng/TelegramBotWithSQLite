import sqlite3
import telebot
from telebot import types
from datetime import datetime

# Bot configuration
API_TOKEN = 'your-api-token'
bot = telebot.TeleBot(API_TOKEN)

# Database setup
def create_tables():
    conn = sqlite3.connect('telgram_bot_data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (user_id INTEGER PRIMARY KEY, username TEXT, subscription_end DATE)''')
    conn.commit()
    conn.close()

def add_user(user_id, username):
    conn = sqlite3.connect('telgram_bot_data.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    if c.fetchone() is None:
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

# Command handlers
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Hello! Use the /profile command to view your profile.')

@bot.message_handler(commands=['profile'])
def profile(message):
    user_id = message.from_user.id
    username = message.from_user.username

    # Add user to the database if not already present
    add_user(user_id, username)

    user = get_user_profile(user_id)
    if user:
        username, subscription_end = user
        days_left = calculate_days_left(subscription_end)
        if days_left < 0:
            subscription_status = 'Your subscription has expired.'
        else:
            subscription_status = f'Days left: {days_left}'
        bot.reply_to(message, f'Profile:\nUsername: {username}\n{subscription_status}')
    else:
        bot.reply_to(message, 'Error retrieving profile information.')

# Start the bot
def main():
    create_tables()  # Create tables if they do not exist
    bot.polling()

if __name__ == '__main__':
    main()
