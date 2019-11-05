import bcrypt
import config
from random import choice
import sqlite3


class DB:
    def __init__(self, base=config.data_base_name):
        conn = sqlite3.connect(base, check_same_thread=False)
        self.conn = conn

    def get_connection(self):
        return self.conn

    def __del__(self):
        self.conn.close()


def encrypt_password(new_password):
    password = bytes(new_password, encoding='utf-8')
    s = bcrypt.gensalt(12)
    hashed_password = bcrypt.hashpw(password, s)
    return hashed_password


def check_password_correctness(password):
    invalid_combinations = 'qwertyuiop asdfghjkl zxcvbnm йцукенгшщзхъ фывапролджэё ячсмитьбю'
    letter = 0
    big_letter = 0
    number = 0
    for i in password:
        if i.isalpha():
            letter += 1
        if i.isalpha() and i.upper() == i:
            big_letter += 1
        if i.isdigit():
            number += 1
    invalid = 0
    for j in range(len(password) - 2):
        if password[j:j + 3].lower() in invalid_combinations:
            invalid += 1
    if len(password) < 9:
        return "Пароль слишком короткий("
    if letter == 0 or big_letter == 0:
        return "Пароль должен содержать и большие и маленькие буквы("
    if number == 0:
        return "В пароле должны быть цифры("
    if invalid != 0:
        return "Это слишком очевидный пароль("
    return "OK"


def create_user_dictionary(data):
    dictionary = {'user_id': None, 'chat_id': None, 'user_login': None, 'user_password': None, 'user_surname': None,
                  'user_name': None,'user_second_name': None, 'user_photo': None, 'user_department': None,
                  'user_section': None, 'user_position': None, 'self_info': None, 'access_level': None,
                  'last_seen': None, 'last_try': None,'telegram_link': None,}
    i = 0
    for key in dictionary:
        dictionary[key] = data[i]
        i += 1
    return dictionary


def generate_login_password():
    letters = 'abcdefghijklmnopqrstuvwxyz'
    numbers = '0123456789'
    all = 'abcdefghijklmnopqrstuvwxyz0123456789'
    login = 'mgt_'
    base = DB()
    connection = base.get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT user_id, user_name FROM users")
    id = []
    for i in cursor.fetchall():
        id.append(i[0])
    login += str(max(id) + 1)
    password = choice(list(letters)).upper()
    for i in range(8):
        password += choice(list(all))
    password += choice(list(numbers))
    base.__del__()
    return login, password

