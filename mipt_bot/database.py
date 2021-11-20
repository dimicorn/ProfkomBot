import sqlite3
from datetime import datetime, timedelta
import pandas as pd


def check_verification(message):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    # Getting user's email
    username = message.from_user.username
    query = f"SELECT * FROM users WHERE username='{username}'"
    cursor.execute(query)
    data = cursor.fetchone()
    if data is None:
        return False
    else:
        return True


def add_code(message, code, email):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    query = f'INSERT INTO verification VALUES ("{message.from_user.username}", "{code}", 0, "{email}")'
    cursor.execute(query)
    conn.commit()


def check_code(message):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    username = message.from_user.username
    query = f"SELECT * FROM verification WHERE username='{username}'"
    cursor.execute(query)
    code = cursor.fetchone()[1]
    return code


def add_attempt(message):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    username = message.from_user.username
    query = f"SELECT * FROM verification WHERE username='{username}'"
    cursor.execute(query)
    attempts = cursor.fetchone()[2]

    if attempts == 3:
        return False
    else:
        query = f"UPDATE verification SET attempts = {attempts + 1} WHERE username = '{username}'"
        cursor.execute(query)
        conn.commit()
        return True


def ban_user(message):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")

    query = f'INSERT INTO ban VALUES ("{message.from_user.username}", "{tomorrow}")'
    cursor.execute(query)
    conn.commit()


def check_ban(message):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    query = f"SELECT * FROM ban WHERE username='{message.from_user.username}'"
    cursor.execute(query)
    data = cursor.fetchone()
    if data is None:
        return False
    else:
        dateString = data[1]
        dateFormatter = "%Y-%m-%d %H:%M:%S"
        end_date = datetime.strptime(dateString, dateFormatter)
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        dateString1 = now
        dateFormatter1 = "%Y-%m-%d %H:%M:%S"
        now_date = datetime.strptime(dateString1, dateFormatter1)
        if now_date > end_date:
            query = f"DELETE FROM ban WHERE username = '{message.from_user.username}'"
            cursor.execute(query)
            conn.commit()
            return False
        else:
            remain = (end_date - now_date)
            return remain


def add_user(message):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    # Getting user's email
    username = message.from_user.username
    query = f"SELECT * FROM verification WHERE username='{username}'"
    cursor.execute(query)

    email = cursor.fetchone()[3]

    fio, group = get_users_name(email)
    fio_list = fio.split(' ')
    if len(fio_list) == 2:
        surname = fio_list[0]
        name = fio_list[1]
    elif len(fio_list) == 3:
        surname = fio_list[0]
        name = fio_list[1]
        second_name = fio_list[2]

    query = f'INSERT INTO users VALUES ("{username}", "{email}", "{surname}", "{group}", "{name}", "{second_name}")'
    cursor.execute(query)
    conn.commit()

    query = f"DELETE FROM verification WHERE username = '{username}'"
    cursor.execute(query)
    conn.commit()


def get_users_name(post):
    data = pd.read_excel('data/students-2.xlsx')
    fio = list(data['ФИО'])
    email = list(data['e-mail'])
    group = list(data['Группа'])

    for i in range(len(email)):
        if email[i] == post:
            return fio[i], group[i]


def get_visits(message):
    user_surname, user_group, user_name, user_second_name = get_users_data(message)

    data = pd.read_excel('data/fight.xlsx')

    fio = list(data['ФИО'])
    visits = list(data['пос-я'])
    group = list(data['неделя'])

    for i in range(len(fio)):
        if i > 1:
            fio_list = fio[i].split(' ')
            surname = fio_list[0]
            name = fio_list[1]

            if surname == user_surname and name == user_name and group[i - 1] == user_group:
                return int(visits[i])


def get_users_data(message):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    username = message.from_user.username
    query = f"SELECT * FROM users WHERE username='{username}'"
    cursor.execute(query)
    data = cursor.fetchone()
    surname = data[2]
    group = data[3]
    name = data[4]
    second_name = data[5]
    return surname, group, name, second_name
