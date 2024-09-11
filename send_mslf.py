import telebot
import sqlite3
import tokens

connection = sqlite3.connect('db.db', check_same_thread=False)
cursor = connection.cursor()


TOKEN = tokens.token_bot
bot = telebot.TeleBot(TOKEN)

text_to_send = ''

while text_to_send != 'stop':
    text_to_send = str(input())
    cursor.execute("""SELECT * FROM UsersNIT""")
    records = cursor.fetchall()

    for row in records:
        try:
            bot.send_message(row[1], text_to_send)
            print(f'message was sent to {row[1]}')
        except:
            print(f"can't send to {row[1]}")


bot.polling(none_stop=True, interval=0, timeout=10)
