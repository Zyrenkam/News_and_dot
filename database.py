import sqlite3
from datetime import datetime
connection = sqlite3.connect('db.db', check_same_thread=False)
cursor = connection.cursor()


def create_db():
    cursor.execute('''CREATE TABLE IF NOT EXISTS UsersNIT ( 
        id_tg TEXT,
        chat_id TEXT,
        name TEXT, 
        settings TEXT,
        subscription INTEGER,
        violations INTEGER,
        feedback VARCHAR(254)
    )
    ''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS  CooperationUsers (
        id_tg TEXT,
        chat_id TEXT,
        name TEXT,
        date DATETIME ,
        connect TEXT
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS BlackList (
        id_tg TEXT,
        chat_id TEXT, 
        name TEXT, 
        date TEXT
    )''')
    connection.commit()
    print('DB CREATED')


def add_user(id_tg, chat_id, name, settings, subscription, violations, feedback):
    flag = True
    cursor.execute("""SELECT id_tg from UsersNIT""")
    records = cursor.fetchall()
    for row in records:
        if id_tg == row[0]:
            flag = False

    if flag:
        cursor.execute('INSERT INTO UsersNIT (id_tg, chat_id, name, settings, subscription, violations, feedback) VALUES'
                       ' (?, ?, ?, ?, ?, ?, ?)', (id_tg, chat_id, name, settings, subscription, violations, feedback))
        connection.commit()
    print('USER ADDED')


def is_sub(id_tg):
    cursor.execute('''SELECT id_tg FROM UsersNIT''')
    records = cursor.fetchall()

    for row in records:
        if row[0] == id_tg:
            return True

    return False


def del_user(id_tg):
    cursor.execute('DELETE FROM UsersNIT WHERE id_tg = ?', (id_tg, ))
    connection.commit()
    print('USER DELETED')


def change_settings(id_tg, settings):
    cursor.execute('UPDATE UsersNIT SET settings = ? WHERE id_tg = ?', (settings, id_tg))
    connection.commit()
    print('SETTINGS CHANGED')


def update_subscription(type='day_passed', points=0, id_tg='user'):
    cursor.execute("""SELECT * from UsersNIT""")
    records = cursor.fetchall()

    if type == 'day_passed':
        for row in records:
            cursor.execute('UPDATE UsersNIT SET subscription = subscription-1 WHERE id_tg = ?', (row[0], ))
            cursor.execute('UPDATE UsersNIT SET subscription = 0 WHERE subscription <= 0')
            connection.commit()
    elif type == 'add_bonus':
        cursor.execute('UPDATE UsersNIT SET subscription = subscription + ? WHERE id_tg = ?', (points, id_tg))
        connection.commit()
    elif type == 'rm_day':
        cursor.execute('UPDATE UsersNIT SET subscription = subscription - ? WHERE id_tg = ?', (points, id_tg))
        connection.commit()

    print('SUBS UPDATED')


def get_list_id():
    id_list = []
    cursor.execute("""SELECT chat_id from UsersNIT""")
    records = cursor.fetchall()

    for row in records:
        id_list.append(row[0])

    return id_list


def have_sub(chat_id):
    cursor.execute("""SELECT * from UsersNIT""")
    records = cursor.fetchall()

    for row in records:
        if (row[1] == chat_id) and (int(row[4]) > 0):
            print(chat_id, row[4])
            return True

    return False


def get_settings(chat_id):
    cursor.execute("""SELECT * from UsersNIT""")
    records = cursor.fetchall()

    for row in records:
        if row[1] == chat_id:
            return row[3]


def counter_set(type, id_tg):
    cursor.execute("SELECT * FROM UsersNIT")
    records = cursor.fetchall()

    for row in records:
        if row[0] == id_tg:
            if type == 'sub':
                return row[4]
            elif type == 'viol':
                return row[5]


def add_feedback(id_tg, text):
    cursor.execute("UPDATE UsersNIT SET feedback = feedback || ? WHERE id_tg = ?", (text, id_tg))
    connection.commit()
    print('FEEDBACK SAVED')


def add_violations(id_tg, count):
    cursor.execute("UPDATE UsersNIT SET violations = violations + ? WHERE id_tg = ?", (count, id_tg))
    connection.commit()

    print('VIOLATION UPDATED')


def add_cooperation(id_tg, chat_id, name, connect='-'):
    date = datetime.now()
    unix_date = date.timestamp()

    flag1 = True
    to_new_resp = int()

    cursor.execute('SELECT id_tg, date FROM CooperationUsers')
    records = cursor.fetchall()

    for row in records:
        if row[0] == id_tg:
            unix_date2 = datetime.strptime(str(row[1]), "%Y-%m-%d %H:%M:%S").timestamp()

            #проверка, прошло ли 3 дня
            if (unix_date - unix_date2) < 3 * 86400:
                to_new_resp = int(unix_date - unix_date2) / 86400
                flag1 = False

    if flag1:
        cursor.execute('INSERT INTO CooperationUsers (id_tg, chat_id, name, date, connect) VALUES (?, ?, ?, ?, ?)',
                       (id_tg, chat_id, name, str(date)[:19:], connect))
        connection.commit()
        print('COOPERATION USER ADDED')
        return 0
    else:
        print('FORBIDDEN TO COOPERATE', to_new_resp)
        return round(to_new_resp, 1)


def check_black_list():
    cursor.execute("""SELECT * FROM UsersNIT """)
    records = cursor.fetchall()

    for row in records:
        if int(row[5]) >= 20:
            cursor.execute("SELECT id_tg FROM BlackList WHERE id_tg=?", (row[0],))
            rez = cursor.fetchall()

            if not rez:
                cursor.execute(
                    'INSERT INTO BlackList (id_tg, chat_id, name, date) VALUES'
                    ' (?, ?, ?, ?)', (row[0], row[1], row[2], str(datetime.datetime.now())[:19]))
                connection.commit()
                print('ADDED TO BLAK LIST')
            else:
                print('ALREADY IN BLACK LIST')


def cancellation_violation():
    cursor.execute('SELECT violations FROM UsersNIT')
    cursor.execute('UPDATE UsersNIT SET violations = 0')
    connection.commit()

    print('CANCELLATION DONE')


def close_connection():
    connection.commit()
    connection.close()
    print('DB CLOSED CONNECTION')
