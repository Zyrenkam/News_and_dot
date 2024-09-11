import time
import telebot
import schedule
from threading import Thread
from telebot import types
from time import sleep
import random
import parser_news
from database import *
import make_foto
import tokens

TOKEN = tokens.token_bot
bot = telebot.TeleBot(TOKEN)

bot.set_my_commands([
    telebot.types.BotCommand('/start', 'Запуск бота'), telebot.types.BotCommand('/help', 'Помощь'),
    telebot.types.BotCommand('/change_settings', 'Изменение настроек новостей'),
    telebot.types.BotCommand('/feedback', 'Отставить отзыв'), telebot.types.BotCommand('/bonus', 'Бонусная программа'),
    telebot.types.BotCommand('/reference', 'Информация о подписке'),
    telebot.types.BotCommand('/cooperation', 'Сотрудничество'), telebot.types.BotCommand('/violations', 'Информация о нарушениях'),
    telebot.types.BotCommand('/rules', 'Правила канала и бота')]
)

#for channel
CHANNEL_NAME = '@Dot_And_News'

#for dialog
chat_id = get_list_id()
url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"

list_of_rubrics = {'Экономика': 0, 'Политика': 1, 'Спорт': 2, 'Технологии': 3, 'Религия': 4}
users_rubrics = list()

emotions = ['🔎', '🔴', '🔵', '⚪️', '💸', '🔔', '💬', '💭', '🗯', '🔊', '🚩', '📣', '📢', '📊', '📉', '📈', '📆', '🔬',
     '🔭', '⌛️', '🪙', '⚡️', '✨', '🗾', '🌆', '🌇', '🎆', '🎇', '🌠', '🌄', '🌅', '🏞', '🎑', '🏙', '🌃', '🌌',
     '🌉', '🌁', '🏛', '🖥', '💾', '📪', '📫', '📬', '📭', '📥', '📤', '📦', '📮', '📯', '📜', '📃', '📄', '📑',
     '🧾', '🗒', '🗓', '📇', '🗃', '🗄', '📋', '📁', '📂', '🗂', '🗞', '📰', '📓', '📔', '📒', '📕', '📗', '📘',
     '📙', '📚', '📖', '🔖', '🧮', '🧷', '🔗', '📎', '🖇', '📝', '📌', '📍', '📛', '⛔️', '❗️', '❕', '❓',
     '❔', '❌', '⭕️', '‼️', '⁉️', '〽️', '⚠️', '🚸', '✅', '❇️', '✳️', '❎', '🌐', '☑️', '🔘', '🟠', '🟡',
     '🟢', '🟣', '⚫️', '🟤', '🔺', '🔻', '🔸', '🔹', '🔶', '🔷', '🔳', '🔲', '▪️', '▫️', '◾️', '◽️', '◼️',
     '◻️', '🟥', '🟧', '🟨', '🟩', '🟦', '🟫', '⬜️', '⬛️', '🟪', '🔇', '🔕', '♦️', '🕐', '🕑', '🕒', '🕓',
     '🕜', '🕛', '🕘', '🕠', '🕟']


def schedule_checker():
    while True:
        schedule.run_pending()
        sleep(1)


def send_news_to_channel():
    prev_new = ''

    list_of_news = parser_news.create_answer()
    print(list_of_news)

    random_new = list(list_of_news.keys())[random.randint(0, len(list_of_news.keys())-1)]

    res = f'{emotions[random.randint(0, len(emotions)-1)]} ' + random_new.upper() +\
          f' {emotions[random.randint(0, len(emotions)-1)]} ' + '\n \n' + list_of_news[random_new].split('|')[0]

    if res != prev_new:
        print(list_of_news[random_new].split('|'))
        bot.send_photo(CHANNEL_NAME, list_of_news[random_new].split('|')[1], res)
        #bot.send_message(CHANNEL_NAME, res)
        prev_new = res
    else:
        send_news_to_channel()

    print('NEWS ON CHANNEL')


def send_news_to_user():
    message = 'НОВОСТНАЯ СВОДКА!'

    photo = str()

    list_of_news = parser_news.create_answer()
    print(list_of_news)

    for i in range(0, len(chat_id)):
        print(chat_id[i], not have_sub(chat_id[i]))

        #проверка наличия подписки
        if not have_sub(chat_id[i]):
            message = 'Тут могли бы быть любимые новости, но у Вас нет подписки, либо она закончилась. Вы можете ее легко и быстро приобрести'
        else:
            rubrics = get_settings(chat_id[i]).split()
            for type in rubrics:
                print(type)
                #0 - ec, 1 - pol, 2- спорт, 3 - технологии 4 - religion
                new_key = list(list_of_news.keys())[int(type)]
                message = '\n \n' + f'{emotions[random.randint(0, len(emotions) - 1)]} ' + new_key.upper() +\
                           f' {emotions[random.randint(0, len(emotions)-1)]} ' '\n'\
                           + list_of_news[new_key].split('|')[0]
                photo = list_of_news[new_key].split('|')[1]

                try:
                    bot.send_photo(chat_id[i], photo, message)
                except:
                    print('ERROR with', chat_id[i])
                time.sleep(10)

    print('NEWS IN CHAT BOT')


def send_weather_courses():
    print("CREATING FOTO")
    make_foto.make_foto()
    print("FOTO DONE")
    img = open('foto_post/output.png', 'rb')
    bot.send_photo(CHANNEL_NAME, img, 'Всем удачного дня и хорошего настроения!')


def bot_advertising():
    text = 'Чтобы получать больше интересных новостей, а также иметь возможность настройки уведомлений под себя \n' \
           'Переходите по ссылке в бота и пользуйтесь на здоровье, пожалуйста! \n' \
           'https://t.me/News_And_Dot_bot'
    bot.send_message(CHANNEL_NAME, text)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    print(message)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in range(0, len(list(list_of_rubrics.keys())), 2):
        if i == 4:
            markup.add(types.KeyboardButton(list(list_of_rubrics.keys())[i]))
        else:
            markup.add(types.KeyboardButton(list(list_of_rubrics.keys())[i]), types.KeyboardButton(list(list_of_rubrics.keys())[i+1]))
    btn_stop = types.KeyboardButton('Закончить редактирование')
    markup.add(btn_stop)

    bot.send_message(message.chat.id,
                     text="Здрaвствуйте, {0.first_name}! Я новостной бот! Выберите рубрики,"
                          " по которым Вы хотите получать больше новостей".format(
                         message.from_user), reply_markup=markup)


@bot.message_handler(commands=['help'])
def help_msg(message):
    bot.send_message(message.chat.id, '/start \n /help \n /change_settings \n /feedback \n /bonus '
                                      '\n /reference \n /cooperation \n /violations \n /rules')


@bot.message_handler(commands=['rules'])
def rules(message):
    bot.send_message(message.chat.id, 'Правила пользования ботом и каналом')
    doc = open('Правила от 14.04.2024.pdf', 'rb')
    bot.send_document(message.chat.id, doc)


@bot.message_handler(commands=['cooperation'])
def cooperation(message):
    print(message.from_user.username, '|', str(message.chat.id), '|', message.from_user.first_name)
    res_to_add_cooper = add_cooperation(str(message.from_user.username), str(message.chat.id), str(message.from_user.first_name))
    if res_to_add_cooper == 0:
        bot.send_message(message.chat.id, 'Запрос отправлен, с Вами свяжутся в ближайшее время!')
    else:
        bot.send_message(message.chat.id, f'Отказано в доступе, пожалуйста, подождите {res_to_add_cooper} дн.')


@bot.message_handler(commands=['change_settings'])
def help_change_set(message):
    send_welcome(message)


@bot.message_handler(commands=['reference'])
def reference(message):
    bot.send_message(message.chat.id, f"Длительность подписки (дней): {counter_set('sub', message.from_user.username)}")


@bot.message_handler(commands=['violations'])
def violations(message):
    bot.send_message(message.chat.id, f'Количество нарушений: {counter_set("viol", message.from_user.username)}')


@bot.message_handler(commands=['feedback'])
def feedback(message):
    bot.send_message(message.chat.id, 'Пожалуйста, напишите все что думаете о проекте.'
                                      ' Нам реально интересно услышать Ваше мнение, чтобы сделать его лучше! \n '
                                      'Напишите согласно следующему формату: \n '
                                      'Отзыв: Ваш отзыв')
    print('FEEDBACK: ', message.text)


@bot.message_handler(commands=['bonus'])
def bonus_info(message):
    bot.send_message(message.chat.id, 'Существует возможность получения бонусов за различную активность на канале'
                                      ' (оставление отзыва, комментария, реакций). 1 очко = 1 день подписки'
                                      '\n отзыв - 5 очков, '
                                      '\n реакция - 0.1 очка,'
                                      '\n комментарий - 0.3 очка, '
                                      '\n приглашение друга - 7 очков, '
                                      '\n идеи по развитию проекта - 15 очков')


@bot.message_handler(func=lambda message: True)
def processing(message):
    print(message.from_user.username, '|', message.from_user.first_name, '|', message.from_user.last_name, '|', message.text)

    if message.text in list_of_rubrics.keys():
        users_rubrics.append(message.text)
        bot.send_message(message.chat.id, f'Вы добавили раздел "{message.text}"')
    elif message.text == 'Закончить редактирование':
        temp_rubrics = list(set(users_rubrics))

        bot.send_message(message.chat.id, f'Вы успешно добавили следующие разделы {temp_rubrics}. При возникновении вопросов напишите /help',
                         reply_markup=types.ReplyKeyboardRemove())

        for i in range(0,  len(users_rubrics)):
            try:
                temp_rubrics[i] = str(list_of_rubrics[users_rubrics[i]])
            except:
                pass

        print(message.from_user.username, '|', message.from_user.first_name, '|', ' '.join(temp_rubrics), '|', 0)
        add_user(str(message.from_user.username), str(message.chat.id), str(message.from_user.first_name) + ' ' +
                 str(message.from_user.last_name), ' '.join(temp_rubrics), 0, 0, ' ')
        change_settings(str(message.from_user.username), ' '.join(temp_rubrics))
        del users_rubrics[:]

    if message.text.lower()[0:5:] == 'отзыв':
        review = str(message.text.lower()).replace('отзыв', '') + ' |\n'
        add_feedback(message.from_user.username, review)
        update_subscription('add_bonus', 5, message.from_user.username)
        bot.send_message(message.chat.id, 'Ваш отзыв очень ценен для нас и будет сохранен')


schedule.every().day.at("07:00").do(send_weather_courses)

#для канала отправка в 11:00, 14:00, 17:00, 20:00. Для бота 10:00, 13:00, 16:00, 19:00, 22:00
try:
    schedule.every(3).hours.at("10:00").until("22:01").do(send_news_to_user)
    schedule.every(3).hours.at("11:00").until("20:01").do(send_news_to_channel)
except:
    pass

schedule.every().day.at("19:00").do(bot_advertising)

schedule.every().day.at("00:00").do(update_subscription)
schedule.every().day.at("00:00").do(check_black_list)

schedule.every().monday.at("10:00").do(cancellation_violation)

'''schedule.every().day.at("17:08").do(send_news_to_user)
schedule.every().day.at("17:08").do(send_news_to_channel)'''

send_weather_courses()

Thread(target=schedule_checker).start()

bot.polling(none_stop=True, interval=0, timeout=10)
