import telebot
from check_msg import *
import database as db
import tokens

token = tokens.token_controller_bot
bot = telebot.TeleBot(token)

chat_id = tokens.chat_id_controller_bot


@bot.message_handler(func=lambda message: True)
def command(message):
    user_id = message.from_user.id
    msg = message.text
    msg_id = message.id
    print(user_id, '|', msg, '|', msg_id)

    if check_msg(msg):
        #если сообщение не из канала и не мое  and (user_id != 136817688)
        if (user_id != 777000):
            #отправляем ответ на комментарий
            print('OK')

            if db.is_sub(message.from_user.username):
                db.update_subscription('add_bonus', 0.3, str(message.from_user.username))
            else:
                # добавление пользователя и увеличение подписки
                db.add_user(str(message.from_user.username), '0000000000', str(message.from_user.first_name) + ' ' +
                    str(message.from_user.last_name), ' ', 0, 0, ' ')
                db.update_subscription('add_bonus', 0.3, str(message.from_user.username))

    else:
        #применение штрафа
        if db.is_sub(message.from_user.username):
            db.update_subscription('rm_day', 1, str(message.from_user.username))
            db.add_violations(str(message.from_user.username), 1)
        else:
            db.add_user(str(message.from_user.username), str(message.chat.id), str(message.from_user.first_name) + ' ' +
                        str(message.from_user.last_name), ' ', 0, 0, ' ')
            db.update_subscription('rm_day', 1, str(message.from_user.username))
            db.add_violations(str(message.from_user.username), 1)

        delete_msg(msg_id)


def delete_msg(msg_id):
    bot.delete_message(chat_id, msg_id)
    print('MESSAGE DELETED')


#bot.polling(none_stop=True)
bot.polling(none_stop=True, interval=0, timeout=10)
