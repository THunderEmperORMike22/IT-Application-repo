import config
import telebot
import bcrypt
from datetime import datetime
from telebot import types
from time import sleep
from Bot_Special_Functions import send_photo, send_keyboard, send_url_keyboard, bot_greeting, \
    check_time, unexpected_message
from Bot_DB_Functions import encrypt_password, check_password_correctness, create_user_dictionary, DB, \
    generate_login_password


bot = telebot.TeleBot(config.token)

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!CLASSES!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


class BotDB:
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS chats
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                             chat_id INTEGER,
                             last_try INTEGER
                             )""")
        cursor.close()
        self.connection.commit()

    def insert_chat(self, chat_id):
        cursor = self.connection.cursor()
        new_time = int(datetime.today().timestamp())
        cursor.execute("""INSERT INTO chats
                          (chat_id, last_try) VALUES (?,?)""", (chat_id, new_time))
        cursor.close()
        self.connection.commit()

    def get_chat_info(self, chat_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT last_try FROM chats WHERE chat_id = ?", (chat_id,))
        row = cursor.fetchone()
        cursor.close()
        self.connection.commit()
        if row:
            return row
        else:
            return None

    def update_info(self, chat_id):
        cursor = self.connection.cursor()
        new_time = int(datetime.today().timestamp())
        cursor.execute("UPDATE chats SET last_try = ? WHERE chat_id = ?", (new_time, chat_id))
        cursor.close()
        self.connection.commit()


class BotLinks:
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS links
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                             link_name VARCHAR,
                             link_description VARCHAR,
                             url_address VARCHAR
                             )""")
        cursor.close()
        self.connection.commit()

    def get_link(self, link_name):
        cursor = self.connection.cursor()
        cursor.execute("SELECT link_description, url_address FROM links WHERE link_name = ?", (link_name,))
        row = cursor.fetchone()
        cursor.close()
        self.connection.commit()
        if row:
            return row
        else:
            return None

    def update_link(self, link_name, new_link):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE links SET url_address = ? WHERE link_name = ?", (new_link, link_name))
        cursor.close()
        self.connection.commit()


class User:
    def __init__(self, connection):
        self.connection = connection

    def user_error(self, error, error_values):
        error_message = "Ошибка в Боте!!!\n\n" + str(error) + "\n\n" + "Последние введённые данные:\n" + \
                        "\n".join(error_values)
        bot.send_message(519433230, error_message)
        return None

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS users
                            (user_id INTEGER PRIMARY KEY AUTOINCREMENT, chat_id INTEGER, user_login VARCHAR(50),
                            user_password VARCHAR(128), user_surname VARCHAR(50), user_name VARCHAR(50),
                            user_second_name VARCHAR(50), user_photo VARCHAR, user_department VARCHAR,
                            user_section VARCHAR, user_position VARCHAR, self_info VARCHAR, access_level INTEGER,
                            last_seen INTEGER, last_try INTEGER, telegram_link VARCHAR)""")
        cursor.close()
        self.connection.commit()

    def check_for_existence_id(self, user_id):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
            row = cursor.fetchone()
            return True if row else False
        except Exception as e:
            self.user_error(e, [user_id])
            return "Error"

    def check_for_existence_login(self, user_login):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM users WHERE user_login = ?", (user_login,))
            row = cursor.fetchone()
            return True if row else False
        except Exception as e:
            self.user_error(e, [user_login])
            return "Error"

    def check_for_existence_surname(self, user_surname):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM users WHERE user_surname = ?", (user_surname,))
            row = cursor.fetchone()
            return True if row else False
        except Exception as e:
            self.user_error(e, [user_surname])
            return "Error"

    def check_password_match(self, user_login, password):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT user_password FROM users WHERE user_login = ?", (user_login,))
            true_password = cursor.fetchone()[0]
            if true_password:
                if bcrypt.checkpw(bytes(password, encoding="utf-8"), true_password):
                    return True
            return False
        except Exception as e:
            self.user_error(e, [user_login, password])
            return "Error"

    def check_login_free(self, login):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT user_id FROM users WHERE user_login = ?", (login,))
            row = cursor.fetchone()
            return False if row else True
        except Exception as e:
            self.user_error(e, [login])
            return "Error"

    def change_password(self, user_login, old_password, new_password):
        try:
            cursor = self.connection.cursor()
            is_password_correct = check_password_correctness(new_password)
            check = self.check_for_existence_login(user_login)
            if check is True:
                if is_password_correct == "OK":
                    if self.check_password_match(user_login, old_password):
                        new_password = encrypt_password(new_password)
                        cursor.execute("UPDATE users SET user_password = ? WHERE user_login = ?",
                                       (new_password, user_login))
                        cursor.close()
                        self.connection.commit()
                        return "Пароль успешно изменён!"
                    else:
                        return "ОШИБКА! Неправильно введён старый пароль!"
                else:
                    return is_password_correct
            elif check is False:
                return "ОШИБКА! Данный пользователь не существует!"
            elif check == "Error":
                return config.user_error_message
        except Exception as e:
            self.user_error(e, [user_login, old_password, new_password])
            return config.user_error_message

    def change_login(self, user_id, new_login):
        try:
            cursor = self.connection.cursor()
            if self.check_login_free(new_login):
                cursor.execute("UPDATE users SET user_login = ? WHERE user_id = ?", (new_login, user_id))
                cursor.close()
                self.connection.commit()
                return True
            else:
                return False
        except Exception as e:
            self.user_error(e, [user_id, new_login])
            return "Error"

    def change_self_information(self, user_id, new_information):
        try:
            cursor = self.connection.cursor()
            cursor.execute("UPDATE users SET self_info = ? WHERE user_id = ?", (new_information, user_id))
            cursor.close()
            self.connection.commit()
            return True
        except Exception as e:
            self.user_error(e, [user_id, new_information])
            return "Error"

    def get_user_by_login(self, user_login):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM users WHERE user_login = ?", (user_login,))
            row = cursor.fetchone()
            return row
        except Exception as e:
            self.user_error(e, [user_login])
            return "Error"

    def get_user_by_id(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        return row

    def get_user_by_name(self, user_name):
        try:
            name = user_name.lower().split()
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM users WHERE user_surname = ? AND user_name = ? AND user_second_name = ?",
                           (name[0], name[1], name[2]))
            row = cursor.fetchone()
            return row
        except Exception as e:
            self.user_error(e, [user_name])
            return "Error"

    def get_user_by_chat(self, chat_id):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM users WHERE chat_id = ?", (chat_id,))
            row = cursor.fetchone()
            return row
        except Exception as e:
            self.user_error(e, [chat_id])
            return "Error"

    def check_authorization(self, chat_id):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT last_seen, last_try FROM users WHERE chat_id = ?", (chat_id,))
            row = cursor.fetchone()
            if row:
                return row
            else:
                return None
        except Exception as e:
            self.user_error(e, [chat_id])
            return "Error"


# Добавить Исключения
class Admin(User):
    def insert_user(self, user_surname, user_name, user_second_name, user_login, password, user_photo, user_department,
                    user_section, user_position, access_level):
        cursor = self.connection.cursor()
        password_hash = encrypt_password(password)
        cursor.execute("""INSERT INTO users
                          (user_login, user_password, user_surname, user_name, user_second_name, user_photo,
                          user_department, user_section, user_position, access_level) VALUES (?,?,?,?,?,?,?,?,?,?)""",
                       (user_login, password_hash, user_surname, user_name, user_second_name, user_photo,
                        user_department, user_section, user_position,
                        access_level))
        cursor.close()
        self.connection.commit()

    def get_multiple_users(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        return rows

    def delete_user(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute("""DELETE FROM users WHERE user_id = ?""", (user_id,))
        cursor.close()
        self.connection.commit()
        return True


class Administer(Admin):
    def __init__(self, bot, information):
        self.base = DB()
        super().__init__(self.base.get_connection())
        self.bot = bot
        self.admin_info = information
        self.admin_access = self.admin_info["access_level"]
        self.login = None
        self.password = None
        self.photo = None
        self.user_surname = None
        self.user_name = None
        self.user_second_name = None
        self.user_department = None
        self.user_section = None
        self.user_position = None
        self.access_level = None
        self.link_for_change = None

    def admin_menu(self, message, bot_message="Чем я могу помочь?", admin_help=False):
        if admin_help:
            sleep(1)
            if self.admin_access >= 3:
                self.bot.send_message(message.chat.id, config.admin_menu_help_message.format(config.admin_menu_links_message))

            else:
                self.bot.send_message(message.chat.id, config.admin_menu_help_message.format(""))
        sleep(1)
        '''if self.admin_access >= 3:
            msg = send_keyboard(self.bot, message, ["🔄Ссылки", "📋Меню", "📨Рассылка", "✅Добавить пользователя",
                                                    "❎Удалить пользователя", "🆘Помощь"], bot_message, True)
        else:'''
        msg = send_keyboard(self.bot, message, ["🆘Помощь", "📋Меню", "📨Рассылка", "✅Добавить пользователя",
                                                    "❎Удалить пользователя"], bot_message, True)
        self.bot.register_next_step_handler(msg, self.admin_menu_functions)

    def admin_menu_functions(self, message):
        if message.text == "📋Меню":
            self.base.__del__()
            main_menu(message)
        elif message.text == "🆘Помощь":
            self.admin_menu(message, bot_message="Чем я могу помочь?", admin_help=True)
        elif message.text == "🔄Ссылки":
            links_list = ""
            base = DB(config.links_base_name)
            link_connection = base.get_connection()
            link_cursor = link_connection.cursor()
            link_cursor.execute("SELECT link_name, link_description FROM links")
            links = link_cursor.fetchall()
            for _ in links:
                links_list += "• " + str("*" + _[0] + "*") + " - " + _[1] + "\n"
            link_cursor.close()
            link_connection.commit()
            base.__del__()
            self.bot.send_message(message.chat.id, config.links_change_message.format(links_list), parse_mode="Markdown")
            msg = send_keyboard(self.bot, message, ["🔙Отмена"], "Введите название Информации/Ссылки, "
                                                                "которую хотите изменить")
            self.bot.register_next_step_handler(msg, self.insert_link_for_change)
        elif message.text == "✅Добавить пользователя":
            keyboard = send_keyboard(self.bot, message, ["🔙Отмена"], "Введите ФИО добавляемого пользователя")
            self.bot.register_next_step_handler(keyboard, self.start_insert_user)
        elif message.text == "❎Удалить пользователя":
            keyboard = send_keyboard(self.bot, message, [config.user_list, "🔙Отмена"], config.bot_user_delete)
            self.bot.register_next_step_handler(keyboard, self.start_delete)
        elif message.text == "📨Рассылка":
            mail = Mailing(bot, self.admin_info)
            mail.start_mailing(message)
        elif message.text == "/start":
            start(message)
        elif message.text == "/menu":
            entrance(message)
        else:
            self.bot.send_message(message.chat.id, unexpected_message())
            self.admin_menu(message)

    def insert_link_for_change(self, message):
        if message.text == "🔙Отмена":
            self.admin_menu(message)
        else:
            self.link_for_change = message.text
            msg = send_keyboard(self.bot, message, ["🔙Отмена"], "Введите новую Информацию/Cсылку")
            self.bot.register_next_step_handler(msg, self.change_link)

    def change_link(self, message):
        if message.text == "🔙Отмена":
            self.admin_menu(message)
        elif message.text == "/start":
            start(message)
        elif message.text == "/menu":
            entrance(message)
        else:
            base = DB(config.links_base_name)
            link_connection = base.get_connection()
            link_changer = BotLinks(link_connection)
            link_changer.update_link(self.link_for_change, message.text)
            link_connection.commit()
            base.__del__()
            self.bot.send_message(message.chat.id, "Информация/Ссылка успешно изменена")
            self.admin_menu(message)

    def start_insert_user(self, message):
        if message.text == "🔙Отмена":
            self.admin_menu(message)
        elif message.text == "/start":
            start(message)
        elif message.text == "/menu":
            entrance(message)
        else:
            user_info = message.text.lower().split()
            self.user_surname = user_info[0]
            self.user_name = user_info[1]
            self.user_second_name = user_info[2]
            self.bot.send_message(message.chat.id, config.bot_user_insert)
            keyboard = send_keyboard(self.bot, message, ["🎰Сгенерировать", "🔙Отмена"], config.generate_button_help)
            self.bot.register_next_step_handler(keyboard, self.insert_login_password)

    def insert_login_password(self, message):
        if message.text == "🔙Отмена":
            self.admin_menu(message)
        elif message.text == "/start":
            start(message)
        elif message.text == "/menu":
            entrance(message)
        else:
            if message.text == "🎰Сгенерировать":
                self.login, self.password = generate_login_password()
            else:
                self.login, self.password = message.text.split()
            bot.send_message(message.chat.id, "Загрузите фото добавляемого пользователя в формате jpg (как фото)")
            msg = send_keyboard(self.bot, message, ["⏩Пропустить", "🔙Отмена"], config.skip_button_help)
            self.bot.register_next_step_handler(msg, self.insert_photo)

    def insert_photo(self, message):
        if message.text == "🔙Отмена":
            self.admin_menu(message)
        elif message.text == "/start":
            start(message)
        elif message.text == "/menu":
            entrance(message)
        elif message.text == "⏩Пропустить":
            self.photo = "photos/Empty.jpg"
            self.insert_work_info(message)
        else:
            try:
                photo_info = self.bot.get_file(message.photo[len(message.photo) - 1].file_id)
                downloaded_photo = self.bot.download_file(photo_info.file_path)
                self.photo = config.photo_adress + photo_info.file_path + str(self.admin_info["user_id"])
                with open(self.photo, "wb") as new_photo:
                    new_photo.write(downloaded_photo)
                self.insert_work_info(message)
            except Exception:
                self.bot.send_message(message.chat.id, "Что-то пошло не так, попробуйте ещё раз")
                msg = send_keyboard(self.bot, message, ["⏩Пропустить", "🔙Отмена"],
                                    "Загрузите фото добавляемого пользователя в формате jpg (как фото)")
                self.bot.register_next_step_handler(msg, self.insert_photo)

    def insert_work_info(self, message):
        if self.admin_access == 1:
            self.user_department = self.admin_info["user_department"]
            self.user_section = self.admin_info["user_section"]
            msg = send_keyboard(self.bot, message, ["🔙Отмена"], "Введите должность добавляемого пользователя")
            self.bot.register_next_step_handler(msg, self.insert_position)
        elif self.admin_access == 2:
            self.user_department = self.admin_info["user_department"]
            cursor = self.connection.cursor()
            cursor.execute("SELECT DISTINCT user_section FROM users WHERE user_department = ?",
                           (self.admin_info["user_department"],))
            buttons = []
            if cursor.fetchall():
                for i in cursor.fetchall():
                    buttons.append(i[0])
            buttons.append("🔙Отмена")
            msg = send_keyboard(self.bot, message, buttons, "Выберете отдел или введите новый", True)
            self.bot.register_next_step_handler(msg, self.insert_section)
        else:
            cursor = self.connection.cursor()
            cursor.execute("SELECT DISTINCT user_department FROM users")
            row = cursor.fetchall()
            buttons = []
            bot_message = ""
            if row:
                for i in row:
                    buttons.append(i[0])
                    bot_message = "Выберете управление или введите новое"
            else:
                bot_message = "Введите управление"
            buttons.append("🔙Отмена")
            msg = send_keyboard(self.bot, message, buttons, bot_message, True)
            self.bot.register_next_step_handler(msg, self.insert_department)

    def insert_department(self, message):
        if message.text == "🔙Отмена":
            self.admin_menu(message)
        elif message.text == "/start":
            start(message)
        elif message.text == "/menu":
            entrance(message)
        else:
            self.user_department = message.text
            cursor = self.connection.cursor()
            cursor.execute("SELECT DISTINCT user_section FROM users WHERE user_department = ?",
                           (self.user_department,))
            raw = cursor.fetchall()
            buttons = []
            bot_message = ""
            if raw:
                for i in raw:
                    buttons.append(i[0])
                    bot_message = "Выберете отдел или введите новый"
            else:
                bot_message = "Введите отдел"
            buttons.append("🔙Отмена")
            msg = send_keyboard(self.bot, message, buttons, bot_message, True)
            self.bot.register_next_step_handler(msg, self.insert_section)

    def insert_section(self, message):
        if message.text == "🔙Отмена":
            self.admin_menu(message)
        elif message.text == "/start":
            start(message)
        elif message.text == "/menu":
            entrance(message)
        else:
            self.user_section = message.text
            msg = send_keyboard(self.bot, message, ["🔙Отмена"], "Введите должность добавляемого пользователя")
            self.bot.register_next_step_handler(msg, self.insert_position)

    def insert_position(self, message):
        if message.text == "🔙Отмена":
            self.admin_menu(message)
        elif message.text == "/start":
            start(message)
        elif message.text == "/menu":
            entrance(message)
        else:
            self.user_position = message.text
            buttons = []
            i = 0
            while i < self.admin_access:
                buttons.append(str(i))
                i += 1
            buttons.append("🔙Отмена")
            msg = send_keyboard(self.bot, message, ["🔙Отмена"], config.access_level_message)
            self.bot.register_next_step_handler(msg, self.insert_access_level)

    def insert_access_level(self, message):
        if message.text == "🔙Отмена":
            self.admin_menu(message)
        elif message.text == "/start":
            start(message)
        elif message.text == "/menu":
            entrance(message)
        else:
            self.access_level = int(message.text)
            if (self.access_level < self.admin_access < 3) or \
                    (self.admin_access == 3 and self.access_level <= self.admin_access):
                self.insert_user(self.user_surname, self.user_name, self.user_second_name, self.login, self.password,
                                 self.photo, self.user_department, self.user_section, self.user_position,
                                 self.access_level)
                self.bot.send_message(message.chat.id, "Пользователь успешно добавлен!")
                user = create_user_dictionary(self.get_user_by_name(self.user_surname + " " + self.user_name + " " +
                                                                    self.user_second_name))
                bot.send_message(message.chat.id, "Информация о пользователе:")
                bot.send_message(message.chat.id, "login:\t\t{}\npassword:\t\t{}".format(self.login, self.password))
                bot.send_message(message.chat.id, config.user_information_message.format(user["user_id"],
                                                                                         user["user_surname"] + " " +
                                                                                         user["user_name"] + " " +
                                                                                         user["user_second_name"],
                                                                                         user["user_department"],
                                                                                         user["user_section"],
                                                                                         user["user_position"]))
                self.login = None
                self.password = None
                self.photo = None
                self.user_name = None
                self.user_department = None
                self.user_section = None
                self.user_position = None
                self.access_level = None
                self.admin_menu(message, "Чем я могу ещё помочь?")
            else:
                bot.send_message(message.chat.id, "Вы не можете предоставить сотруднику данный уровень доступа :("
                                                  "Попробуйте ещё раз")
                self.insert_position(self.bot.send_message(message.chat.id, self.user_position))

    def start_delete(self, message):
        if message.text == config.user_list:
            users_list = UsersList(bot, self.admin_info, "delete_list")
            users_list.delete_list(message)
        elif message.text == "🔙Отмена":
            self.admin_menu(message)
        elif message.text == "/start":
            start(message)
        elif message.text == "/menu":
            entrance(message)
        else:
            self.admin_delete_user(message)

    def admin_delete_user(self, message):
        if message.text == "🔙Отмена":
            self.admin_menu(message)
        elif message.text == "/start":
            start(message)
        elif message.text == "/menu":
            entrance(message)
        else:
            if str(message.text[0]) in "1234567890":
                id = message.text
                check = self.check_for_existence_id(id)
                if check:
                    self.delete_user(id)
                    self.user_department = None
                    self.user_section = None
                    bot.send_message(message.chat.id, "Пользователь успешно удалён")
                    self.admin_menu(message)
                else:
                    self.bot.send_message(message.chat.id, "Такого пользователя нет :( Попробуйте ещё раз")
                    self.start_delete(message)
            else:
                name = message.text
                surname = name.split()[0]
                check = self.check_for_existence_surname(surname)
                if check:
                    self.delete_user(self.get_user_by_name(name)[0])
                    self.user_department = None
                    self.user_section = None
                    bot.send_message(message.chat.id, "Пользователь успешно удалён")
                    self.admin_menu(message)
                else:
                    self.bot.send_message(message.chat.id, "Такого пользователя нет :( Попробуйте ещё раз")
                    self.start_delete(message)


class Authorization(User):
    def __init__(self, bot, menu):
        self.base = DB()
        super().__init__(self.base.get_connection())
        self.bot = bot
        self.count = 3
        self.login = None
        self.res = None
        self.return_menu = menu

    def start_authorization(self, message, bot_message="Введите логин"):
        msg = send_keyboard(self.bot, message, ["🔙Отмена"], bot_message)
        self.bot.register_next_step_handler(msg, self.login_answer)

    def login_answer(self, message):
        if message.text == "🔙Отмена":
            if self.return_menu == "start":
                start_menu(message, False)
            else:
                guest_menu(message, False)
        elif message.text == "/start":
            start(message)
        elif message.text == "/menu":
            entrance(message)
        else:
            self.login = message.text.strip()
            login_existence = self.check_for_existence_login(self.login)
            if login_existence is True:
                self.ask_for_password(message)
            elif login_existence is False:
                error_message = "Упс, Неверный логин( Попробуйте ещё раз"
                self.start_authorization(message, error_message)
            else:
                send_exception(message)

    def ask_for_password(self, message, bot_message="Введите пароль"):
        msg = send_keyboard(self.bot, message, ["🔙Отмена"], bot_message)
        bot.register_next_step_handler(msg, self.password_answer)

    def password_answer(self, message):
        if message.text == "🔙Отмена":
            if self.return_menu == "start":
                start_menu(message, False)
            else:
                guest_menu(message, False)
        elif message.text == "/start":
            start(message)
        elif message.text == "/menu":
            entrance(message)
        else:
            password = message.text
            password_match = self.check_password_match(self.login, password)
            if password_match is True:
                cursor = self.connection.cursor()
                new_time = int(datetime.today().timestamp())
                cursor.execute("UPDATE users SET last_seen = ? WHERE user_login = ?", (new_time, self.login))
                self.connection.commit()
                if message.from_user.username:
                    link = "https://t.me/" + message.from_user.username
                    cursor.execute("UPDATE users SET telegram_link = ? WHERE user_login = ?", (link, self.login))
                    self.connection.commit()
                cursor.execute("UPDATE users SET chat_id = ? WHERE user_login = ?", (message.chat.id, self.login))
                self.connection.commit()
                cursor.execute("UPDATE users SET last_try = ? WHERE user_login = ?", (new_time, self.login))
                self.connection.commit()
                cursor.execute("SELECT user_surname, user_name, user_second_name FROM users WHERE user_login = ?",
                               (self.login,))
                row = cursor.fetchone()
                if row:
                    if row[0] and row[1] and row[2]:
                        name = ", " + row[1].capitalize() + " " + row[2].capitalize() + "!"
                    else:
                        name = ", " + row[0].capitalize() + " " + row[1].capitalize() + "!"
                else:
                    name = "!"
                cursor.close()
                self.connection.commit()
                self.base.__del__()
                self.bot.send_message(message.chat.id, "Добро пожаловать{}".format(name))
                sleep(1)
                main_menu(message, "Чем я могу помочь?", True)
            elif password_match is False:
                if self.count > 0:
                    error_message = "Неверный пароль( Попробуйте снова"
                    self.count -= 1
                    self.ask_for_password(message, error_message)
                else:
                    cursor = self.connection.cursor()
                    new_time = int(datetime.today().timestamp())
                    cursor.execute("UPDATE users SET last_try = ? WHERE user_login = ?", (new_time, self.login))
                    new_base = DB(config.bot_base_name)
                    bot_connection = new_base.get_connection()
                    bot_base = BotDB(bot_connection)
                    bot_base.update_info(message.chat.id)
                    new_base.__del__()
                    cursor.close()
                    self.connection.commit()
                    self.base.__del__()
                    if self.return_menu == "start":
                        start_menu(message, False, config.password_limit_message + "минуту.")
                    else:
                        guest_menu(message, False, config.password_limit_message + "минуту.")
            else:
                send_exception(message)


class PersonalAccount(User):
    def __init__(self, bot):
        self.base = DB()
        super().__init__(self.base.get_connection())
        self.bot = bot
        self.information = None
        self.old_password = None

    def account_menu(self, message):
        self.information = get_user_information(message)
        msg = send_keyboard(self.bot, message, ["🔄Логин", "🔄Пароль", "🔄Фото",
                                                "🔄О себе", "📋Меню", "📴Выход"],
                            "Чем я могу помочь?", True)
        self.bot.register_next_step_handler(msg, self.account_menu_functions)

    def account_menu_functions(self, message):
        if message.text == "📋Меню":
            self.base.__del__()
            main_menu(message)
        elif message.text == "🔄Логин":
            msg = send_keyboard(self.bot, message, ["🔙Отмена"], "Введите новый логин")
            self.bot.register_next_step_handler(msg, self.account_change_login)
        elif message.text == "🔄Пароль":
            msg = send_keyboard(self.bot, message, ["🔙Отмена"], "Введите старый пароль")
            self.bot.register_next_step_handler(msg, self.account_get_old_password)
        elif message.text == "🔄О себе":
            if self.information["self_info"]:
                self.bot.send_message(message.chat.id, "Вот ваша текущая личная информация:")
                old_info_message = self.information["self_info"]
                self.bot.send_message(message.chat.id, old_info_message)
            self.bot.send_message(message.chat.id, "Введите новую")
            msg = send_keyboard(self.bot, message, ["🔙Отмена"], config.self_information_help_message)
            self.bot.register_next_step_handler(msg, self.account_change_self_info)
        elif message.text == "🔄Фото":
            msg = send_keyboard(self.bot, message, ["🔙Отмена"], "Загрузите новое фото в формате jpg (как фото)")
            self.bot.register_next_step_handler(msg, self.change_photo)
        elif message.text == "📴Выход":
            self.exit(message)
        elif message.text == "/start":
            start(message)
        elif message.text == "/menu":
            entrance(message)
        else:
            self.bot.send_message(message.chat.id, unexpected_message())
            self.account_menu(message)

    def account_change_login(self, message):
        if message.text == "🔙Отмена":
            self.account_menu(message)
        elif message.text == "/start":
            start(message)
        elif message.text == "/menu":
            entrance(message)
        else:
            change = self.change_login(self.information["user_id"], message.text)
            if change is True:
                self.bot.send_message(message.chat.id, "Поздравляю! Логин успешно изменён!")
                self.account_menu(message)
            elif change is False:
                self.bot.send_message(message.chat.id, "Вас опередили! Такой логин уже существует :(")
                msg = send_keyboard(self.bot, message, ["Да", "Нет"], "Попробовать ещё раз?", True)
                self.bot.register_next_step_handler(msg, self.account_invalid_login)
            else:
                send_exception(message)

    def account_get_old_password(self, message):
        if message.text == "🔙Отмена":
            self.account_menu(message)
        elif message.text == "/start":
            start(message)
        elif message.text == "/menu":
            entrance(message)
        else:
            self.old_password = message.text
            password_match = self.check_password_match(self.information["user_login"], self.old_password)
            if password_match is True:
                msg = send_keyboard(self.bot, message, ["🔙Отмена"], "Введите новый пароль")
                self.bot.register_next_step_handler(msg, self.account_change_password)
            elif password_match is False:
                self.bot.send_message(message.chat.id, "Неправильно введён старый пароль!")
                msg = send_keyboard(self.bot, message, ["Да", "Нет"], "Попробовать ещё раз?", True)
                self.bot.register_next_step_handler(msg, self.account_invalid_password)
            else:
                send_exception(message)

    def account_change_password(self, message):
        if message.text == "🔙Отмена":
            self.account_menu(message)
        elif message.text == "/start":
            start(message)
        elif message.text == "/menu":
            entrance(message)
        else:
            new_password = message.text
            change = self.change_password(self.information["user_login"], self.old_password, new_password)
            if change == "Пароль успешно изменён!":
                self.bot.send_message(message.chat.id, change)
                self.account_menu(message)
            else:
                self.bot.send_message(message.chat.id, change + "\nПопробуйте ещё раз")
                msg = send_keyboard(self.bot, message, ["🔙Отмена"], "Введите новый пароль")
                self.bot.register_next_step_handler(msg, self.account_change_password)

    def account_change_self_info(self, message):
        if message.text == "🔙Отмена":
            self.account_menu(message)
        elif message.text == "/start":
            start(message)
        elif message.text == "/menu":
            entrance(message)
        else:
            change = self.change_self_information(self.information["user_id"], message.text)
            if change is True:
                self.bot.send_message(message.chat.id, "Информация успешно изменена!")
                self.account_menu(message)
            else:
                send_exception(message)

    def account_invalid_login(self, message):
        if message.text == "Да":
            msg = self.bot.send_message(message.chat.id, "Введите новый логин")
            self.bot.register_next_step_handler(msg, self.account_change_login)
        elif message.text == "/start":
            start(message)
        elif message.text == "/menu":
            entrance(message)
        else:
            self.account_menu(message)

    def account_invalid_password(self, message):
        if message.text == "Да":
            msg = send_keyboard(self.bot, message, ["🔙Отмена"], "Введите старый пароль")
            self.bot.register_next_step_handler(msg, self.account_get_old_password)
        elif message.text == "/start":
            start(message)
        elif message.text == "/menu":
            entrance(message)
        else:
            self.account_menu(message)

    def change_photo(self, message):
        try:
            if message.text == "🔙Отмена":
                self.account_menu(message)
            elif message.text == "/start":
                start(message)
            elif message.text == "/menu":
                entrance(message)
            else:
                user = get_user_information(message)
                photo_info = self.bot.get_file(message.photo[len(message.photo) - 1].file_id)
                downloaded_photo = self.bot.download_file(photo_info.file_path)
                if user["user_photo"] and user["user_photo"] != "photos/Empty.jpg":
                    with open(user["user_photo"], "wb") as new_photo:
                        new_photo.write(downloaded_photo)
                else:
                    photo = config.photo_adress + photo_info.file_path + str(self.information["user_id"])
                    with open(photo, "wb") as new_photo:
                        new_photo.write(downloaded_photo)
                    if not user["user_photo"]:
                        cursor = self.connection.cursor()
                        cursor.execute("UPDATE users SET user_photo = ? WHERE user_id = ?", (photo, user["user_id"]))
                        cursor.close()
                        self.connection.commit()
                self.bot.send_message(message.chat.id, "Фото успешно изменено!")
                self.account_menu(message)
        except Exception as e:
            self.user_error(e)
            self.bot.send_message(message.chat.id, "Что-то пошло не так, попробуйте ещё раз")
            msg = send_keyboard(self.bot, message, ["🔙Отмена"], "Загрузите новое фото в формате jpg (как фото)")
            self.bot.register_next_step_handler(msg, self.change_photo)

    def exit(self, message):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE users SET last_seen = ? WHERE user_login = ?", (None, self.information["user_login"]))
        self.connection.commit()
        cursor.execute("UPDATE users SET chat_id = ? WHERE user_login = ?", (None, self.information["user_login"]))
        self.connection.commit()
        cursor.execute("UPDATE users SET last_try = ? WHERE user_login = ?", (None, self.information["user_login"]))
        cursor.close()
        self.connection.commit()
        start_menu(message)


class History:
    def __init__(self, message, bot, menu):
        self.message = message
        self.bot = bot
        self.menu = menu

    def start_history(self, message):
        send_photo(self.bot, message, "Bot_Pictures/Bot_MGT_logo2.png", config.history_message1)
        send_url_keyboard(self.bot, message, "МОСГОРТУР", get_link("mgt_url"),
                              "Перейти на сайт Мосгортур")
        sleep(1.5)
        self.bot.send_message(message.chat.id, config.history_message2)
        sleep(1)
        send_photo(self.bot, message, "Bot_Pictures/Bot_History1.jpg", config.history_message3)
        sleep(1.5)
        self.bot.send_message(message.chat.id, config.history_message4)
        sleep(1)
        self.bot.send_message(message.chat.id, config.history_message5)
        sleep(1)
        send_photo(self.bot, message, "Bot_Pictures/Bot_History2.jpg", config.history_message6)
        sleep(1.5)
        self.bot.send_message(message.chat.id, config.history_message7)
        sleep(1)
        send_photo(self.bot, message, "Bot_Pictures/Bot_History3.png", config.history_message8)
        msg = send_keyboard(bot, message, ["📋Меню"], config.history_message9)
        self.bot.register_next_step_handler(msg, self.end_history)

    def end_history(self, message):
        if message.text == "📋Меню":
            if self.menu == "guest":
                guest_menu(message)
            else:
                main_menu(message)
        elif message.text == "/start":
            start(message)
        elif message.text == "/menu":
            entrance(message)
        else:
            self.bot.send_message(message.chat.id, unexpected_message())
            msg = send_keyboard(bot, message, ["📋Меню"], "Повторите пожалуйста")
            self.bot.register_next_step_handler(msg, self.end_history)


class Services:
    def __init__(self, bot):
        self.bot = bot

    def start_services(self, message):
        if message.text == "📋Меню":
            main_menu(message)
        elif message.text == "/start":
            start(message)
        elif message.text == "/menu":
            entrance(message)
        else:
            msg = send_keyboard(self.bot, message, ["GLPI", "Office 365", "ЭДО", "АИС", "Helpdesk", "📋Меню"],
                                "Вот сервисы, информацию о которых можно получить", True)
            self.bot.register_next_step_handler(msg, self.services_information)

    def services_information(self, message):
        if message.text == "📋Меню":
            main_menu(message)
        elif message.text == "GLPI":
            send_photo(self.bot, message, "Bot_Pictures/Bot_GLPI_logo.jpg", config.glpi_message)
            sleep(1.5)
            bot.send_message(message.chat.id, config.glpi_access)
            send_url_keyboard(self.bot, message, "Перейти на GLPI", get_link("glpi_url"),
                              "Нажмите, чтобы перейти к сервису: ")
            self.more_services(message)
        elif message.text == "Office 365":
            send_photo(self.bot, message, "Bot_Pictures/Bot_Office365_logo.png", config.office_message)
            sleep(1.5)
            send_url_keyboard(self.bot, message, "Перейти на GLPI", get_link("glpi_url"), config.office_install)
            send_url_keyboard(self.bot, message, "Перейти на Office.com", get_link("office_url"),
                              "Узнать больше можно на сайте сервиса: ")
            self.more_services(message)
        elif message.text == "ЭДО":
            send_photo(self.bot, message, "Bot_Pictures/Bot_Edo_logo.jpg", config.edo_message)
            sleep(1.5)
            bot.send_message(message.chat.id, config.edo_install)
            send_url_keyboard(self.bot, message, "Перейти к ЭДО", get_link("glpi_url"),
                              "Нажмите, чтобы перейти к сервису: ")
            self.more_services(message)
        elif message.text == "АИС":
            send_photo(self.bot, message, "Bot_Pictures/Bot_MGT_logo1.png", config.ais_message)
            sleep(1.5)
            bot.send_message(message.chat.id, config.ais_access)
            send_url_keyboard(self.bot, message, "Перейти на АИС", get_link("ais_url"),
                              "Нажмите, чтобы перейти к сервису: ")
            self.more_services(message)
        elif message.text == "Helpdesk":
            send_photo(self.bot, message, "Bot_Pictures/Bot_Helpdesk_logo.png", config.helpdesk_message)
            sleep(1.5)
            bot.send_message(message.chat.id, config.helpdesk_access)
            send_url_keyboard(self.bot, message, "Перейти на Helpdesk", get_link("helpdesk_url"),
                              "Нажмите, чтобы перейти к сервису: ")
            self.more_services(message)
        elif message.text == "/start":
            start(message)
        elif message.text == "/menu":
            entrance(message)
        else:
            self.bot.send_message(message.chat.id, unexpected_message())
            self.start_services(message)

    def more_services(self, message):
        msg = send_keyboard(self.bot, message, ["🎓Узнать больше", "📋Меню"], "Больше о сервисах?", True)
        bot.register_next_step_handler(msg, self.start_services)


class Privileges:
    def __init__(self, bot, menu):
        self.bot = bot
        self.menu = menu

    def start_privileges(self, message):
        if message.text == "📋Меню":
            if self.menu == "guest":
                guest_menu(message)
            else:
                main_menu(message)
        elif message.text == "/start":
            start(message)
        elif message.text == "/menu":
            entrance(message)
        else:
            msg = send_keyboard(self.bot, message, ["☎Связь", "📚Публикации", "🏀⚽Спорт", "☂Страховка", "🎫Путёвки",
                                                    "🇬🇧Английский", "📋Меню"],
                                "Сотрудникам МОСГОРТУР доступны следующие привилегии", True)
            self.bot.register_next_step_handler(msg, self.privileges_information)

    def privileges_information(self, message):
        if message.text == "📋Меню":
            if self.menu == "guest":
                guest_menu(message)
            else:
                main_menu(message)
        elif message.text == "/start":
            start(message)
        elif message.text == "/menu":
            entrance(message)
        elif message.text == "☎Связь":
            send_photo(self.bot, message, "Bot_Pictures/Bot_Megafon_logo.png", config.megafon_message)
            sleep(1.5)
            self.bot.send_message(message.chat.id, config.megafon_package)
            send_url_keyboard(self.bot, message, "Перейти на GLPI", get_link("glpi_url"), config.megafon_access)
            send_url_keyboard(self.bot, message, "МегаФон", get_link("megafon_url"), "Узнать больше на сайте Мегафон:")
            self.more_privileges(message)
        elif message.text == "📚Публикации":
            send_photo(self.bot, message, "Bot_Pictures/Bot_Article_logo.jpg", config.articles_message)
            sleep(1.5)
            self.bot.send_message(message.chat.id, config.articles_access)
            send_url_keyboard(self.bot, message, "Публикация", get_link("articles_example_url"),
                              "Пример нашей публикации:")
            send_url_keyboard(self.bot, message, "Перейти к библиотеке", get_link("articles_library_url"),
                              "Научная электронная библиотека: ")
            self.more_privileges(message)
        elif message.text == "🏀⚽Спорт":
            sport(message, self.menu)
        elif message.text == "☂Страховка":
            insurance(message, self.menu)
        elif message.text == "🎫Путёвки":
            send_photo(self.bot, message, "Bot_Pictures/Bot_Camp.jpg", config.camp_message)
            sleep(1)
            send_url_keyboard(self.bot, message, "Перейти на сайт", get_link("mgt_url"), config.camp_access1)
            self.bot.send_message(message.chat.id, config.camp_access2)
            self.bot.send_message(message.chat.id, config.camp_access3)
            self.more_privileges(message)
        elif message.text == "🇬🇧Английский":
            send_photo(self.bot, message, "Bot_Pictures/Bot_Skyeng_logo.jpg", config.english_message1)
            send_url_keyboard(self.bot, message, "SKYENG", get_link("english_url1"), "Перейти на сайт")
            sleep(1.5)
            self.bot.send_message(message.chat.id, config.english_message2)
            sleep(1)
            self.bot.send_message(message.chat.id, config.english_message3)
            sleep(1)
            self.bot.send_message(message.chat.id, config.english_message4)
            send_url_keyboard(self.bot, message, "Запишитесь на первый пробный урок", get_link("english_url2"),
                              config.english_message5)
            self.more_privileges(message)
        else:
            self.bot.send_message(message.chat.id, unexpected_message())
            self.start_privileges(message)

    def more_privileges(self, message):
        msg = send_keyboard(self.bot, message, ["💎Другие привилегии", "📋Меню"], "Узнать о других привилегиях?", True)
        self.bot.register_next_step_handler(msg, self.start_privileges)


class Sport:
    def __init__(self, bot, menu, club=None):
        self.bot = bot
        self.menu = menu
        self.club = club
        self.user = None
        self.phone = None
        self.date = None
        self.date_of_birth = None
        self.address = None

    def start_sport(self, message):
        send_photo(self.bot, message, "Bot_Pictures/Bot_Sport.jpg")
        msg = send_keyboard(self.bot, message, ["WorldClass", "XFit", "🔙Отмена"], config.sport_message, True)
        self.bot.register_next_step_handler(msg, self.sport_information)

    def sport_information(self, message):
        if message.text == "🔙Отмена":
            privileges(message, self.menu)
        elif message.text == "/start":
            start(message)
        elif message.text == "/menu":
            entrance(message)
        elif message.text == "WorldClass":
            send_photo(self.bot, message, "Bot_Pictures/Bot_WorldClass_logo.jpg")
            sleep(1.5)
            send_url_keyboard(self.bot, message, "🗺Карта клубов", get_link("worldclass_map"),
                              config.worldclass_message)
            base = DB()
            connection = base.get_connection()
            authorizator = User(connection)
            is_authorized = authorizator.check_authorization(message.chat.id)
            if is_authorized:
                sleep(1)
                keyboard = types.InlineKeyboardMarkup()
                keyboard.add(*[types.InlineKeyboardButton(text=name, callback_data="sport_worldclass_{}".format(name))
                               for name in ["Получить текст заявки"]])
                self.bot.send_message(message.chat.id, config.worldclass_access, reply_markup=keyboard)
                self.bot.send_message(message.chat.id, config.worldclass_access3.format(get_link("worldclass_manager")))
            sleep(1)
            send_url_keyboard(self.bot, message, "📄Прайс-лист", get_link("worldclass_pricelist"), "💲Корпоративные цены")
            send_url_keyboard(self.bot, message, "Перейти на сайт", get_link("worldclass_url"),
                              "Больше о World Class на сайте")
            self.more_sport(message)
        elif message.text == "XFit":
            send_photo(self.bot, message, "Bot_Pictures/Bot_Xfit_logo.jpg")
            sleep(1.5)
            send_url_keyboard(self.bot, message, "🗺Карта клубов", get_link("xfit_map"), config.xfit_message)
            base = DB()
            connection = base.get_connection()
            authorizator = User(connection)
            is_authorized = authorizator.check_authorization(message.chat.id)
            if is_authorized:
                sleep(1)
                keyboard = types.InlineKeyboardMarkup()
                keyboard.add(*[types.InlineKeyboardButton(text=name, callback_data="sport_xfit_{}".format(name))
                               for name in ["Получить текст заявки"]])
                self.bot.send_message(message.chat.id, config.xfit_access, reply_markup=keyboard)
                self.bot.send_message(message.chat.id, config.xfit_access3.format(get_link("xfit_manager")))
            sleep(1)
            send_url_keyboard(self.bot, message, "Перейти на сайт", get_link("xfit_url"), "Больше о XFit на сайте")
            self.more_sport(message)
        else:
            self.bot.send_message(message.chat.id, unexpected_message())
            self.start_sport(message)

    def more_sport(self, message):
        msg = send_keyboard(self.bot, message, ["🎾Узнать больше", "💎Привилегии", "📋Меню"],
                            "Больше о спортивных программах?", True)
        self.bot.register_next_step_handler(msg, self.more_sport_answer)

    def more_sport_answer(self, message):
        if message.text == "📋Меню":
            if self.menu == "guest":
                guest_menu(message)
            else:
                main_menu(message)
        elif message.text == "/start":
            start(message)
        elif message.text == "/menu":
            entrance(message)
        elif message.text == "💎Привилегии":
            privileges(message, self.menu)
        elif message.text == "🎾Узнать больше":
            msg = send_keyboard(self.bot, message, ["WorldClass", "XFit", "🔙Отмена"], "О чём хотите узнать?", True)
            self.bot.register_next_step_handler(msg, self.sport_information)
        else:
            pass

    def get_application(self, message):
        self.user = get_user_information(message)["user_surname"].capitalize() + " " + \
                    get_user_information(message)["user_name"].capitalize() + " " + \
                    get_user_information(message)["user_second_name"].capitalize()
        self.bot.send_message(message.chat.id, "❗Для создания заявки мне потребуется информация❗")
        msg = send_keyboard(self.bot, message, ["🔙Отмена"], "Введите свой контактный телефон", True)
        self.bot.register_next_step_handler(msg, self.get_phone)

    def get_phone(self, message):
        if message.text == "🔙Отмена":
            self.more_sport(message)
        elif message.text == "/start":
            start(message)
        elif message.text == "/menu":
            entrance(message)
        else:
            self.phone = message.text
            if self.club == "worldclass":
                msg = send_keyboard(self.bot, message, ["🔙Отмена"], "Введите Вашу дату рождения:", True)
            else:
                send_url_keyboard(self.bot, message, "Клубы", get_link("xfit_map"),
                                  "Выберете клуб, который хотите посещать")
                msg = send_keyboard(self.bot, message, ["🔙Отмена"], "Введите название выбранного клуба "
                                                        "и предполагаемую дату посещения (через пробел)", True)
            self.bot.register_next_step_handler(msg, self.get_info)

    def get_info(self, message):
        if message.text == "🔙Отмена":
            self.more_sport(message)
        elif message.text == "/start":
            start(message)
        elif message.text == "/menu":
            entrance(message)
        else:
            if self.club == "worldclass":
                self.date_of_birth = message.text
            else:
                info = message.text.split()
                self.address = info[0]
                self.date = info[1]
            msg = send_keyboard(self.bot, message, ["Файл", "Сообщение", "🔙Отмена"],
                                "В каком формате Вы хотели бы получить заявку?", True)
            self.bot.register_next_step_handler(msg, self.create_application)

    def create_application(self, message):
        if message.text == "🔙Отмена":
            self.more_sport(message)
        elif message.text == "/start":
            start(message)
        elif message.text == "/menu":
            entrance(message)
        elif message.text == "Файл":
            with open("application_text.txt", "w", encoding="utf-8") as sport_file:
                if self.club == "worldclass":
                    print(config.sport_application_wc.format(self.phone, self.date_of_birth, self.user),
                          file=sport_file)
                else:
                    print(config.sport_application_xfit.format(self.address, self.phone, self.date, self.user),
                          file=sport_file)
            with open("application_text.txt", "rb") as sport_file:
                self.bot.send_message(message.chat.id, "Заявка готова!")
                self.bot.send_document(message.chat.id, sport_file)
            self.more_sport(message)
        elif message.text == "Сообщение":
            self.bot.send_message(message.chat.id, "Заявка готова!")
            if self.club == "worldclass":
                self.bot.send_message(message.chat.id,
                                      config.sport_application_wc.format(self.phone, self.date_of_birth, self.user))
            else:
                self.bot.send_message(message.chat.id,
                                      config.sport_application_xfit.format(self.address,
                                                                           self.phone, self.date, self.user))
            self.more_sport(message)
        else:
            self.bot.send_message(message.chat.id, unexpected_message())
            msg = send_keyboard(self.bot, message, ["Файл", "Сообщение", "🔙Отмена"],
                                "В каком формате Вы хотели бы получить заявку?", True)
            self.bot.register_next_step_handler(msg, self.create_application)


class Insurance:
    def __init__(self, bot, menu):
        self.bot = bot
        self.menu = menu

    def start_insurance(self, message):
        send_photo(self.bot, message, "Bot_Pictures/Bot_PECO_logo.jpg")
        send_url_keyboard(self.bot, message, "PECO", get_link("insurance_url"), config.insurance_message)
        msg = send_keyboard(self.bot, message, ["🚗ОСАГО", "🏥ДМС", "💳Зелёная карта", "🏡Страхование имущества",
                                                "📋Меню"], config.insurance_message2, True)
        self.bot.register_next_step_handler(msg, self.insurance_information)

    def more_insurance(self, message):
        msg = send_keyboard(self.bot, message, ["🎓Узнать больше", "💎Привилегии", "📋Меню"], "Больше о страховании?")
        self.bot.register_next_step_handler(msg, self.more_insurance_answer)

    def more_insurance_answer(self, message):
        if message.text == "📋Меню":
            if self.menu == "guest":
                guest_menu(message)
            else:
                main_menu(message)
        elif message.text == "/start":
            start(message)
        elif message.text == "/menu":
            entrance(message)
        elif message.text == "💎Привилегии":
            privileges(message, self.menu)
        else:
            msg = send_keyboard(self.bot, message, ["🚗ОСАГО", "🏥ДМС", "💳Зелёная карта", "🏡Страхование имущества",
                                                    "📋Меню"], "О чём хотите узнать?", True)
            self.bot.register_next_step_handler(msg, self.insurance_information)

    def insurance_information(self, message):
        if message.text == "🚗ОСАГО":
            send_photo(self.bot, message, "Bot_Pictures/Bot_Osago.jpg", config.osago_message)
            sleep(2.5)
            self.bot.send_message(message.chat.id, config.access_message)
            self.bot.send_message(message.chat.id, config.osago_doc)
            self.bot.send_message(message.chat.id, config.insurance_access.format(get_link("insurance_manager")))
            self.more_insurance(message)
        elif message.text == "🏡Страхование имущества":
            send_photo(self.bot, message, "Bot_Pictures/Bot_House.jpg", config.home_insurance_message)
            sleep(2.5)
            self.bot.send_message(message.chat.id, config.access_message)
            self.bot.send_message(message.chat.id, config.home_insurance_doc)
            self.bot.send_message(message.chat.id, config.insurance_access.format(get_link("insurance_manager")))
            self.more_insurance(message)
        elif message.text == "💳Зелёная карта":
            send_photo(self.bot, message, "Bot_Pictures/Bot_GreenCard.jpg", config.green_card_message)
            sleep(2.5)
            self.bot.send_message(message.chat.id, config.access_message)
            self.bot.send_message(message.chat.id, config.green_card_doc)
            self.bot.send_message(message.chat.id, config.insurance_access.format(get_link("insurance_manager")))
            self.more_insurance(message)
        elif message.text == "🏥ДМС":
            send_photo(self.bot, message, "Bot_Pictures/Bot_DMS.jpg", config.dms_message)
            sleep(2.5)
            send_url_keyboard(self.bot, message, "Перейти на сайт", get_link("dms_url"), config.dms_doc)
            self.bot.send_message(message.chat.id, config.insurance_access.format(get_link("insurance_manager")))
            self.more_insurance(message)
        elif message.text == "📋Меню":
            if self.menu == "guest":
                guest_menu(message)
            else:
                main_menu(message)
        elif message.text == "/start":
            start(message)
        elif message.text == "/menu":
            entrance(message)
        else:
            self.bot.send_message(message.chat.id, unexpected_message())
            self.start_insurance(message)


class UsersList:
    def __init__(self, bot, information, list_type):
        self.base = DB()
        self.connection = self.base.get_connection()
        self.bot = bot
        self.admin_info = information
        self.admin_access = self.admin_info["access_level"]
        self.user_name = None
        self.user_department = None
        self.user_section = None
        self.list_type = list_type

    def delete_list(self, message):
            if self.admin_access == 1:
                self.show_users_list(message, "Пользователи доступные для удаления:\n",
                                     "Нет пользователей доступных для удаления")
            elif self.admin_access == 2:
                keyboard = send_keyboard(self.bot, message, ["Отдел", "Все", "🔙Отмена"], config.section_ask, True)
                self.bot.register_next_step_handler(keyboard, self.list_answer)
            else:
                keyboard = send_keyboard(self.bot, message, ["Управление", "Все", "🔙Отмена"],
                                         config.department_ask, True)
                self.bot.register_next_step_handler(keyboard, self.list_answer)

    def simple_list(self, message):
        keyboard = send_keyboard(self.bot, message, ["Выбрать", "Все", "🔙Отмена"], config.simple_list_ask, True)
        self.bot.register_next_step_handler(keyboard, self.list_answer)

    def list_answer(self, message):
        if message.text == "🔙Отмена":
            if self.list_type == "delete_list":
                admin(message)
            else:
                navigation(message)
        elif message.text == "/start":
            start(message)
        elif message.text == "/menu":
            entrance(message)
        elif message.text == "Все":
            self.show_users_list(message)
        elif message.text == "Отдел":
            cursor = self.connection.cursor()
            cursor.execute("SELECT DISTINCT user_section FROM users WHERE user_department = ?",
                           (self.admin_info["user_department"],))
            buttons = []
            row = cursor.fetchall()
            if row:
                for i in row:
                    buttons.append(i[0])
            buttons.append("🔙Отмена")
            msg = send_keyboard(self.bot, message, buttons, "Выберете отдел", True)
            self.bot.register_next_step_handler(msg, self.get_section)
        elif message.text == "Управление" or message.text == "Выбрать":
            cursor = self.connection.cursor()
            cursor.execute("SELECT DISTINCT user_department FROM users")
            buttons = []
            row = cursor.fetchall()
            if row:
                for i in row:
                    buttons.append(i[0])
            buttons.append("🔙Отмена")
            msg = send_keyboard(self.bot, message, buttons, "Выберете управление", True)
            self.bot.register_next_step_handler(msg, self.get_department)

    def get_department(self, message):
        if message.text == "🔙Отмена":
            if self.list_type == "delete_list":
                admin(message)
            else:
                navigation(message)
        elif message.text == "/start":
            start(message)
        elif message.text == "/menu":
            entrance(message)
        else:
            self.user_department = message.text
            keyboard = send_keyboard(self.bot, message, ["Отдел", "Все", "🔙Отмена"], config.section_ask, True)
            self.bot.register_next_step_handler(keyboard, self.get_department_answer)

    def get_department_answer(self, message):
        if message.text == "🔙Отмена":
            if self.list_type == "delete_list":
                admin(message)
            else:
                navigation(message)
        elif message.text == "/start":
            start(message)
        elif message.text == "/menu":
            entrance(message)
        elif message.text == "Все":
            if self.list_type == "delete_list":
                self.show_users_list(message, "Пользователи доступные для удаления:\n",
                                     "Нет пользователей доступных для удаления")
            else:
                self.show_users_list(message)
        elif message.text == "Отдел":
            cursor = self.connection.cursor()
            cursor.execute("SELECT DISTINCT user_section FROM users WHERE user_department = ?",
                           (self.user_department,))
            buttons = []
            row = cursor.fetchall()
            if row:
                for i in row:
                    buttons.append(i[0])
            buttons.append("🔙Отмена")
            msg = send_keyboard(self.bot, message, buttons, "Выберете отдел", True)
            self.bot.register_next_step_handler(msg, self.get_section)

    def get_section(self, message):
        if message.text == "🔙Отмена":
            if self.list_type == "delete_list":
                admin(message)
            else:
                navigation(message)
        elif message.text == "/start":
            start(message)
        elif message.text == "/menu":
            entrance(message)
        else:
            self.user_section = message.text
            if self.list_type == "delete_list":
                self.show_users_list(message, "Пользователи доступные для удаления:\n",
                                     "Нет пользователей доступных для удаления")
            else:
                self.show_users_list(message)

    def show_users_list(self, message, users_list="Вот доступные пользователи:\n",
                        invalid_message="Здесь пока никого нет :("):
        cursor = self.connection.cursor()
        if self.user_department:
            if self.user_section:
                cursor.execute("SELECT user_id, user_surname, user_name, user_second_name, user_department, "
                               "user_section, user_position FROM users "
                               "WHERE user_department = ? AND user_section = ? AND access_level <= ?",
                               (self.user_department, self.user_section, self.admin_access))
            else:
                cursor.execute("SELECT user_id, user_surname, user_name, user_second_name, user_department, "
                               "user_section, user_position FROM users WHERE user_department = ? AND access_level <= ?",
                               (self.user_department, self.admin_access))
        else:
            if self.user_section:
                cursor.execute("SELECT user_id, user_surname, user_name, user_second_name, user_department, "
                               "user_section, user_position FROM users WHERE user_department = ? AND access_level <= ?",
                               (self.admin_info["user_department"], self.user_section, self.admin_access))
            else:
                if self.admin_access == 3:
                    cursor.execute("SELECT user_id, user_surname, user_name, user_second_name, user_department, "
                                   "user_section, user_position FROM users WHERE user_id <> ?",
                                   (self.admin_info["user_id"],))
                else:
                    cursor.execute("SELECT user_id, user_surname, user_name, user_second_name, user_department, "
                                   "user_section, user_position FROM users WHERE user_department = ? "
                                   "AND user_section = ? AND access_level < ?",
                                   (self.admin_info["user_department"], self.admin_info["user_section"],
                                    self.admin_access))
        row = cursor.fetchall()
        if row:
            users = sorted(row, key=lambda x: (x[4], x[5], x[1], x[2], x[3]))
            department = ""
            section = ""
            for user in users:
                if user[4] != department:
                    department = user[4]
                    users_list += "\n*Управление: {}*\n\n".format(department)
                if user[5] != section:
                    section = user[5]
                    users_list += "\n\t\t*Отдел: {}*\n\n".format(section)
                users_list += config.user_info.format(user[0], user[1].capitalize() + " " + user[2].capitalize() + " "
                                                      + user[3].capitalize(), user[6])
            self.bot.send_message(message.chat.id, users_list, parse_mode="Markdown")
            self.user_department = None
            self.user_section = None
            self.base.__del__()
            if self.list_type == "delete_list":
                admin_obj = Administer(bot, self.admin_info)
                keyboard = send_keyboard(self.bot, message, ["🔙Отмена"], config.bot_user_delete)
                self.bot.register_next_step_handler(keyboard, admin_obj.admin_delete_user)
            else:
                navigation(message)
        else:
            self.bot.send_message(message.chat.id, invalid_message)
            self.user_department = None
            self.user_section = None
            self.base.__del__()
            if self.list_type == "delete_list":
                admin_obj = Administer(bot, self.admin_info)
                keyboard = send_keyboard(self.bot, message, [config.user_list, "🔙Отмена"], config.bot_user_delete)
                self.bot.register_next_step_handler(keyboard, admin_obj.start_delete)
            else:
                navigation(message)


class Mailing:
    def __init__(self, bot, information):
        self.base = DB()
        self.connection = self.base.get_connection()
        self.bot = bot
        self.admin_info = information
        self.admin_access = self.admin_info["access_level"]
        self.departments = {}
        self.access_level = None
        self.users_for_mail = []
        self.mailing_list = []
        self.mailing_message = ""

    def start_mailing(self, message):
            if self.admin_access == 1:
                self.departments[self.admin_info["user_department"]] = [self.admin_info["user_section"]]
                msg = send_keyboard(self.bot, message, [config.user_list, "Все", "🔙Отмена"],
                                    config.mailing_choose_users)
                self.bot.register_next_step_handler(msg, self.start_choose_users)
            elif self.admin_access == 2:
                self.departments[self.admin_info["user_department"]] = []
                msg = send_keyboard(self.bot, message, ["Выбрать отделы", "Выбрать сотрудников", "Все", "🔙Отмена"],
                                    config.mailing_help2, True)
                self.bot.register_next_step_handler(msg, self.second_answer)
            else:
                msg = send_keyboard(self.bot, message, ["Выбрать управления", "Выбрать сотрудников", "Все", "🔙Отмена"],
                                    config.mailing_help3, True)
                self.bot.register_next_step_handler(msg, self.third_answer)

    def third_answer(self, message):
        if message.text == "🔙Отмена":
            admin_obj = Administer(self.bot, self.admin_info)
            self.base.__del__()
            admin_obj.admin_menu(message, "Чем ещё я могу помочь?")
        elif message.text == "/start":
            start(message)
        elif message.text == "/menu":
            entrance(message)
        elif message.text == "Выбрать управления":
            cursor = self.connection.cursor()
            cursor.execute("SELECT DISTINCT user_department FROM users", )
            departments = []
            for i in cursor.fetchall():
                departments.append(i[0])
            self.bot.send_message(message.chat.id, "Введите одно или несколько (через пробел) управлений, "
                                                   "в которые хотите сделать рассылку")
            msg = send_keyboard(self.bot, message, ["🔙Отмена"], "\n".join(departments), True)
            self.bot.register_next_step_handler(msg, self.choose_departments)
        elif message.text == "Выбрать сотрудников":
            cursor = self.connection.cursor()
            cursor.execute("SELECT DISTINCT user_department, user_id FROM users", )
            departments = []
            for i in cursor.fetchall():
                departments.append(i[0])
            for d in departments:
                sections = []
                cursor.execute("SELECT DISTINCT user_section FROM users WHERE user_department = ?", (d,))
                row = cursor.fetchall()
                if row:
                    for i in row:
                        sections.append(i[0])
                self.departments[d] = sections
            msg = send_keyboard(self.bot, message, [config.user_list, "Все", "🔙Отмена"], config.mailing_choose_users)
            self.bot.register_next_step_handler(msg, self.start_choose_users)
        elif message.text == "Все":
            cursor = self.connection.cursor()
            cursor.execute("SELECT DISTINCT user_department FROM users")
            departments = []
            for i in cursor.fetchall():
                departments.append(i[0])
            for d in departments:
                cursor.execute("SELECT DISTINCT user_section FROM users WHERE user_department = ?", (d,))
                row = cursor.fetchall()
                if row:
                    sections = []
                    for s in row:
                        sections.append(s[0])
                else:
                    continue
                self.departments[d] = sections
            self.create_mailing_list(message)

    def second_answer(self, message):
        if message.text == "🔙Отмена":
            admin_obj = Administer(self.bot, self.admin_info)
            self.base.__del__()
            admin_obj.admin_menu(message, "Чем ещё я могу помочь?")
        elif message.text == "/start":
            start(message)
        elif message.text == "/menu":
            entrance(message)
        elif message.text == "Все":
            self.create_mailing_list(message)
        elif message.text == "Выбрать отделы":
            cursor = self.connection.cursor()
            cursor.execute("SELECT DISTINCT user_section FROM users WHERE user_department = ?",
                           (self.admin_info["user_department"],))
            sections = []
            for i in cursor.fetchall():
                sections.append(i[0])
            self.bot.send_message(message.chat.id, "Введите один или несколько (через пробел) отделов, "
                                                   "в которые хотите сделать рассылку")
            msg = send_keyboard(self.bot, message, ["🔙Отмена"], "\n".join(sections), True)
            self.bot.register_next_step_handler(msg, self.choose_sections_second)
        elif message.text == "Выбрать сотрудников":
            msg = send_keyboard(self.bot, message, [config.user_list, "🔙Отмена"], config.mailing_choose_users)
            self.bot.register_next_step_handler(msg, self.start_choose_users)

    def choose_departments(self, message):
        if message.text == "🔙Отмена":
            admin_obj = Administer(self.bot, self.admin_info)
            self.base.__del__()
            admin_obj.admin_menu(message, "Чем ещё я могу помочь?")
        elif message.text == "/start":
            start(message)
        elif message.text == "/menu":
            entrance(message)
        else:
            departments = message.text.split()
            for d in departments:
                self.departments[d] = []
            msg = send_keyboard(self.bot, message, ["Выбрать отделы", "Выбрать сотрудников", "Все", "🔙Отмена"],
                                config.mailing_help2, True)
            self.bot.register_next_step_handler(msg, self.choose_sections_third)

    def choose_sections_second(self, message):
        if message.text == "🔙Отмена":
            admin_obj = Administer(self.bot, self.admin_info)
            self.base.__del__()
            admin_obj.admin_menu(message, "Чем ещё я могу помочь?")
        elif message.text == "/start":
            start(message)
        elif message.text == "/menu":
            entrance(message)
        else:
            self.departments[self.admin_info["user_department"]] = message.text.split()
            msg = send_keyboard(self.bot, message, [config.user_list, "Все", "🔙Отмена"], config.mailing_choose_users)
            self.bot.register_next_step_handler(msg, self.start_choose_users)

    def choose_sections_third(self, message):
        if message.text == "🔙Отмена":
            admin_obj = Administer(self.bot, self.admin_info)
            self.base.__del__()
            admin_obj.admin_menu(message, "Чем ещё я могу помочь?")
        elif message.text == "/start":
            start(message)
        elif message.text == "/menu":
            entrance(message)
        elif message.text == "Выбрать отделы":
            cursor = self.connection.cursor()
            sections_list = "Доступные отделы:\n\n"
            for d in self.departments:
                cursor.execute("SELECT DISTINCT user_section FROM users WHERE user_department = ?", (d,))
                sections_list += "Управление: {}\n\t\tОтделы:\n".format(d)
                row = cursor.fetchall()
                if row:
                    for i in row:
                        if i[0]:
                            sections_list += "\t\t\t\t{}\n".format(i[0])
                sections_list += "\n"
            self.bot.send_message(message.chat.id, "Введите один или несколько отделов, "
                                                   "в которые хотите сделать рассылку в формате:\n"
                                                   "управление1:отдел отдел/управление2:отдел отдел/...")
            msg = send_keyboard(self.bot, message, ["🔙Отмена"], sections_list, True)
            self.bot.register_next_step_handler(msg, self.choose_sections_third_answer)
        elif message.text == "Выбрать сотрудников":
            cursor = self.connection.cursor()
            for d in self.departments:
                sections = []
                cursor.execute("SELECT DISTINCT user_section FROM users WHERE user_department = ?", (d,))
                row = cursor.fetchall()
                if row:
                    for i in row:
                        sections.append(i[0])
                self.departments[d] = sections
            msg = send_keyboard(self.bot, message, [config.user_list, "Все", "🔙Отмена"], config.mailing_choose_users)
            self.bot.register_next_step_handler(msg, self.start_choose_users)
        else:
            self.create_mailing_list(message)

    def choose_sections_third_answer(self, message):
        if message.text == "🔙Отмена":
            admin_obj = Administer(self.bot, self.admin_info)
            self.base.__del__()
            admin_obj.admin_menu(message, "Чем ещё я могу помочь?")
        elif message.text == "/start":
            start(message)
        elif message.text == "/menu":
            entrance(message)
        else:
            cursor = self.connection.cursor()
            departments = {}
            for i in message.text.split("/"):
                a = i.split(":")
                departments[a[0]] = a[1]
            for d in self.departments:
                if d in departments:
                    self.departments[d] = [departments[d]]
                else:
                    sections = []
                    cursor.execute("SELECT DISTINCT user_section FROM users WHERE user_department = ?", (d,))
                    row = cursor.fetchall()
                    if row:
                        for i in row:
                            sections.append(i[0])
                    self.departments[d] = sections
            msg = send_keyboard(self.bot, message, [config.user_list, "Все", "🔙Отмена"], config.mailing_choose_users)
            self.bot.register_next_step_handler(msg, self.start_choose_users)

    def start_choose_users(self, message):
        if message.text == "🔙Отмена":
            admin_obj = Administer(self.bot, self.admin_info)
            self.base.__del__()
            admin_obj.admin_menu(message, "Чем ещё я могу помочь?")
        elif message.text == "/start":
            start(message)
        elif message.text == "/menu":
            entrance(message)
        elif message.text == "Все":
            self.create_mailing_list(message)
        elif message.text == config.user_list:
            cursor = self.connection.cursor()
            users_list = "Пользователи доступные для рассылки:\n"
            for department in self.departments:
                users_list += "\nУправление:\t{}\n\n".format(department)
                if self.departments[department]:
                    for section in self.departments[department]:
                        cursor.execute("SELECT user_id, user_surname, user_name, user_second_name, "
                                       "user_department, user_section, user_position FROM users "
                                       "WHERE user_department = ? AND user_section = ?", (department, section))
                        row = cursor.fetchall()
                        users_list += "\n\t\tОтдел:\t{}\n\n".format(section)
                        if row:
                            for user in row:
                                users_list += config.user_info.format(user[0], user[1].capitalize() + " " +
                                                                      user[2].capitalize() + " " + user[3].capitalize(),
                                                                      user[6])
                else:
                    cursor.execute("SELECT user_id, user_surname, user_name, user_second_name, "
                                   "user_department, user_section, user_position FROM users "
                                   "WHERE user_department = ? ", (department,))
                    users_list += "\nУправление:\t{}\n\n".format(department)
                    row = cursor.fetchall()
                    if row:
                        section = ""
                        for i in row:
                            if i[5] != section:
                                section = i[5]
                                users_list += "\t\tОтдел:\t{}\n\n".format(section)
                            users_list += config.user_info.format(i[0], i[1].capitalize() + " " + i[2].capitalize() +
                                                                  " " + i[3].capitalize(), i[6] + "\n\n")
            self.bot.send_message(message.chat.id, users_list, parse_mode="Markdown")
            msg = send_keyboard(self.bot, message, ["Все", "🔙Отмена"], "Введите id пользователей, "
                                                                       "которым хотите сделать рассылку "
                                                                       "(через пробел)\nПри нажатии на кнопку ""Все"", "
                                                                       "сообщение будет отправлено всем пользователям")
            self.bot.register_next_step_handler(msg, self.start_choose_users)
        else:
            self.users_for_mail = message.text.split()
            self.create_mailing_list(message)

    def create_mailing_list(self, message):
        cursor = self.connection.cursor()
        if self.users_for_mail:
            for id in self.users_for_mail:
                cursor.execute("SELECT chat_id, user_surname, user_name, user_second_name FROM users "
                               "WHERE user_id = ?", (id,))
                row = cursor.fetchone()
                if row[0]:
                    self.mailing_list.append(row[0])
            msg = send_keyboard(self.bot, message, ["🔙Отмена"], "Введите сообщение для рассылки:")
            self.bot.register_next_step_handler(msg, self.get_message)
        else:
            for department in self.departments:
                if self.departments[department]:
                    if self.departments[department]:
                        for section in self.departments[department]:
                            cursor.execute("SELECT chat_id, user_surname, user_name, user_second_name FROM users "
                                           "WHERE user_department = ? "
                                           "AND user_section = ?", (department, section))
                            raw = cursor.fetchall()
                            if raw:
                                for user in raw:
                                    if user[0]:
                                        self.mailing_list.append(user[0])
                else:
                    cursor.execute("SELECT chat_id, user_id FROM users WHERE user_department = ? ", (department,))
                    row = cursor.fetchall()
                    if row:
                        for i in row:
                            if i[0]:
                                self.mailing_list.append(i[0])
            msg = send_keyboard(self.bot, message, ["🔙Отмена"], "Введите сообщение для рассылки:")
            self.bot.register_next_step_handler(msg, self.get_message)

    def get_message(self, message):
        if message.text == "🔙Отмена":
            admin_obj = Administer(self.bot, self.admin_info)
            self.base.__del__()
            admin_obj.admin_menu(message, "Чем ещё я могу помочь?")
        elif message.text == "/start":
            start(message)
        elif message.text == "/menu":
            entrance(message)
        else:
            sender_name = self.admin_info["user_surname"].capitalize() + " " + \
                          self.admin_info["user_name"].capitalize() + " " + \
                          self.admin_info["user_second_name"].capitalize()
            if sender_name in config.mgt_sender_names:
                sender_name = "МОСГОРТУР"
            self.mailing_message = "<b>Рассылка от {}</b>".format(sender_name)
            if self.admin_info["telegram_link"] and sender_name != "МОСГОРТУР":
                self.mailing_message += " @" + self.admin_info["telegram_link"].split("/")[-1]
            self.mailing_message += ":\n\n" + message.text
            self.mailing(message)

    def mailing(self, message):
        self.bot.send_message(message.chat.id, "Подождит пока происходит рассылка, это может занять некоторое время.")
        if self.mailing_list:
            i = 0
            while i < len(self.mailing_list):
                for j in range(29):
                    self.bot.send_message(self.mailing_list[i], self.mailing_message, parse_mode="HTML")
                    if i < len(self.mailing_list) - 1:
                        i += 1
                    else:
                        i += 1
                        break
                sleep(1)
        self.bot.send_message(message.chat.id, "Рассылка завершена.")
        admin_obj = Administer(self.bot, self.admin_info)
        self.base.__del__()
        admin_obj.admin_menu(message, "Чем ещё я могу помочь?")


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!EXCEPTIONS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


def send_exception(message, author=True, error=None):
    if author and error:
        error_message = "Ошибка в Боте!!!\n\n" + str(error) + "\n\n" + "Последние введённые данные:\n" + message + "\n\n" \
                        + "Текст сообщения:\n" + message.text
        bot.send_message(519433230, error_message)
    bot.send_message(message.chat.id, "Упс :( Что-то пошло не так. Сообщение об ошибке отправлено разработчику. "
                                      "Попробуйте ещё раз.")
    entrance(message)


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!SPECIAL!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


def get_user_information(message):
    base = DB()
    connection = base.get_connection()
    user = User(connection)
    info = create_user_dictionary(user.get_user_by_chat(message.chat.id))
    base.__del__()
    return info


def get_link(link_name):
    base = DB(config.links_base_name)
    connection = base.get_connection()
    link_base = BotLinks(connection)
    link = link_base.get_link(link_name)
    base.__del__()
    return link[1]
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!AUTHORIZATION!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


def authorization(message, menu):
    authorizator = Authorization(bot, menu)
    authorizator.start_authorization(message)


def authorization_last_try(message, last_try, menu):
    last_authorization_try = check_time(last_try)
    if last_authorization_try >= 60:
        authorization(message, menu)
    else:
        time_message = str(60 - last_authorization_try) + "сек."
        if menu == "start":
            start_menu(message, False, config.password_limit_message + time_message)
        else:
            guest_menu(message, False, config.password_limit_message + time_message)


@bot.message_handler(commands=["menu"])
def check_authorization(message, menu="start"):
    base = DB()
    connection = base.get_connection()
    user = User(connection)
    is_authorized = user.check_authorization(message.chat.id)
    if is_authorized:
        last_seen = is_authorized[0]
        last_try = is_authorized[1]
        authorization_time = check_time(last_seen)
        if authorization_time < 2592000:
            base.__del__()
            main_menu(message, "Чем я могу помочь?", True)
        else:
            base.__del__()
            bot.send_message(message.chat.id, "В целях безопасности, пожалуйста, пройдите авторизацию повторно")
            authorization_last_try(message, last_try, menu)
    else:
        base.__del__()
        base = DB(config.bot_base_name)
        connection = base.get_connection()
        bot_base = BotDB(connection)
        user = bot_base.get_chat_info(message.chat.id)
        if not user:
            bot_base.insert_chat(message.chat.id)
            user = bot_base.get_chat_info(message.chat.id)
            base.__del__()
            authorization(message, menu)
        else:
            authorization_last_try(message, user[0], menu)


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!MENU FUNCTIONS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


@bot.message_handler(commands=["history"])
def history(message, menu):
    history_obj = History(message, bot, menu)
    history_obj.start_history(message)


@bot.message_handler(commands=["services"])
def services(message):
    services_obj = Services(bot)
    services_obj.start_services(message)


@bot.message_handler(commands=["privileges"])
def privileges(message, menu):
    privileges_obj = Privileges(bot, menu)
    privileges_obj.start_privileges(message)


@bot.message_handler(commands=["sport"])
def sport(message, menu):
    sport_obj = Sport(bot, menu)
    sport_obj.start_sport(message)


@bot.message_handler(commands=["insurance"])
def insurance(message, menu):
    insurance_obj = Insurance(bot, menu)
    insurance_obj.start_insurance(message)


@bot.callback_query_handler(func=lambda button: "sport" in button.data and True)
def sport_application(button):
        if button.data.split("_")[1] == "worldclass":
            sport_obj = Sport(bot, "guest", "worldclass")
            sport_obj.get_application(button.message)
        else:
            sport_obj = Sport(bot, "guest", "xfit")
            sport_obj.get_application(button.message)


@bot.message_handler(commands=["feedback"])
def feedback(message, menu):
    # bot.send_message(message.chat.id, message)
    feedback_message = get_link("feedback_info")
    if menu == "start":
        msg = send_keyboard(bot, message, ["📋Стартовое Меню"], feedback_message)
    elif menu == "guest":
        msg = send_keyboard(bot, message, ["📋Гостевое Меню"], feedback_message)
    else:
        msg = send_keyboard(bot, message, ["📋Меню"], feedback_message)
    bot.register_next_step_handler(msg, feedback_exit)


def feedback_exit(message):
    if message.text == "📋Стартовое Меню":
        start_menu(message, False)
    elif message.text == "📋Гостевое Меню":
        guest_menu(message, False)
    elif message.text == "/start":
        start(message)
    elif message.text == "/menu":
        entrance(message)
    else:
        main_menu(message, "Чем я могу помочь?", False)


@bot.message_handler(commands=["admin"])
def admin(message):
    admin_obj = Administer(bot, get_user_information(message))
    admin_obj.admin_menu(message, "Чем я могу помочь?", True)


@bot.message_handler(commands=["account"])
def personal_account(message):
    bot.send_message(message.chat.id, config.account_help_message)
    account = PersonalAccount(bot)
    account.account_menu(message)


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!NAVIGATION!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


@bot.message_handler(commands=["navigation"])
def start_navigation(message, bot_message=config.navigation_message):
    msg = send_keyboard(bot, message, ["👫Сотрудники", "📋Меню"], bot_message, True)
    bot.register_next_step_handler(msg, navigation)


def navigation(message):
    if message.text == "📋Меню":
        main_menu(message)
    elif message.text == "/start":
        start(message)
    elif message.text == "/menu":
        entrance(message)
    else:
        msg = send_keyboard(bot, message, [config.user_list, "🔙Отмена"],
                            "Введите id или ФИО сотрудника, о котором хотите узнать")
        bot.register_next_step_handler(msg, user_search)


def user_search(message):
    if message.text == "🔙Отмена":
        start_navigation(message)
    elif message.text == "/start":
        start(message)
    elif message.text == "/menu":
        entrance(message)
    elif message.text == config.user_list:
        info = get_user_information(message)
        info["access_level"] = 3
        users_list = UsersList(bot, info, "simple_list")
        users_list.simple_list(message)
    else:
        base = DB()
        connection = base.get_connection()
        user = User(connection)
        if message.text[0] in "1234567890":
            info = user.get_user_by_id(int(message.text))
        else:
            info = user.get_user_by_name(message.text)
        if info:
            info = create_user_dictionary(info)
            name = info["user_surname"].capitalize() + " " + info["user_name"].capitalize() + " " + \
                info["user_second_name"].capitalize()
            name_message = "{}\n\n• Управление: {}\n• Отдел: {}\n• Должность: {}".format(name,
                                                                                         info["user_department"],
                                                                                         info["user_section"],
                                                                                         info["user_position"])
            if info["user_photo"]:
                send_photo(bot, message, info["user_photo"], name_message)
            if info["self_info"]:
                bot.send_message(message.chat.id, info["self_info"])
            else:
                bot.send_message(message.chat.id, "Этот пользователь ещё не рассказал ничего о себе :(")
            if info["telegram_link"]:
                send_url_keyboard(bot, message, "Написать в Telegram:", info["telegram_link"],
                                  "Чат с @{}:".format(info["telegram_link"].split("/")[-1]))
            base.__del__()
            msg = send_keyboard(bot, message, ["Да", "📋Меню"],
                                "Хотите узнать ещё что-нибудь?", True)
            bot.register_next_step_handler(msg, navigation_answer)
        else:
            bot.send_message(message.chat.id, "Такого пользователя нет(")
            base.__del__()
            msg = send_keyboard(bot, message, ["Да", "📋Меню"],
                                "Хотите узнать ещё что-нибудь?", True)
            bot.register_next_step_handler(msg, navigation_answer)


def navigation_answer(message):
    if message.text == "📋Меню":
        main_menu(message)
    elif message.text == "/start":
        start(message)
    elif message.text == "/menu":
        entrance(message)
    else:
        navigation(message)


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!START and MENU!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, bot_greeting())
    msg = send_keyboard(bot, message, ["Начать"], config.description, True)
    bot.register_next_step_handler(msg, start_button)


def start_button(message):
    entrance(message)


def start_menu(message, start_help=False, bot_message=config.start_authorization_message):
    if start_help:
        bot.send_message(message.chat.id, bot_message)
        msg = send_keyboard(bot, message, ["🚪Вход", "🚶Войти как гость", "💬Обратная связь"],
                            config.start_menu_message, True)
    else:
        msg = send_keyboard(bot, message, ["🚪Вход", "🚶Войти как гость", "💬Обратная связь"], bot_message, True)
    bot.register_next_step_handler(msg, start_menu_answer)


def start_menu_answer(message):
    if message.text == "🚪Вход":
        check_authorization(message, "start")
    elif message.text == "/start":
        start(message)
    elif message.text == "/menu":
        entrance(message)
    elif message.text == "🚶Войти как гость":
        guest_menu(message, True)
    elif message.text == "💬Обратная связь":
        feedback(message, "start")
    else:
        start_menu(message, False, unexpected_message())


def guest_menu(message, guest_help=False, bot_message="Чем я могу помочь?"):
    if guest_help:
        bot.send_message(message.chat.id, config.guest_menu_help_message)
    msg = send_keyboard(bot, message, ["📜История", "💎Привилегии", "💬Обратная связь", "🚪Вход"], bot_message, True)
    bot.register_next_step_handler(msg, guest_menu_functions)


def guest_menu_functions(message):
    if message.text == "🚪Вход":
        check_authorization(message, "guest")
    elif message.text == "/start":
        start(message)
    elif message.text == "/menu":
        entrance(message)
    elif message.text == "📜История":
        history(message, "guest")
    elif message.text == "💎Привилегии":
        privileges(message, "guest")
    elif message.text == "💬Обратная связь":
        feedback(message, "guest")
    else:
        guest_menu(message, False, unexpected_message())


def main_menu(message, bot_message="Чем я могу помочь?", send_help=False):
    information = get_user_information(message)
    greeting_messages = ["привет", "здравствуй", "хай", "хеллоу", "хэллоу", "здравствуйте", "hello", "hi"]
    if message.text.lower() in greeting_messages or message.text.lower()[:-1] in greeting_messages:
        bot.send_message(message.chat.id, bot_greeting())
    if information["access_level"] == 0:
        if send_help:
            bot.send_message(message.chat.id, config.menu_user_help_message)
            sleep(1)
        msg = send_keyboard(bot, message, ["📜История", "💻Сервисы", "💎Привилегии", "🌍Навигация",
                                           "🏠Личный кабинет", "💬Обратная связь"], bot_message, True)
    else:
        if send_help:
            bot.send_message(message.chat.id, config.menu_admin_help_message)
            sleep(1)
        msg = send_keyboard(bot, message, ["📜История", "💻Сервисы", "💎Привилегии", "🌍Навигация",
                                           "🏠Личный кабинет", "💬Обратная связь", "👑Администрирование"],
                            bot_message, True)
    bot.register_next_step_handler(msg, menu_functions)


def menu_functions(message):
    if message.text == "📜История":
        history(message, "main")
    elif message.text == "💻Сервисы":
        services(message)
    elif message.text == "💎Привилегии":
        privileges(message, "main")
    elif message.text == "💬Обратная связь":
        feedback(message, "main")
    elif message.text == "🏠Личный кабинет":
        personal_account(message)
    elif message.text == "🌍Навигация":
        start_navigation(message)
    elif message.text == "👑Администрирование":
        admin(message)
    elif message.text == "/start":
        start(message)
    elif message.text == "/menu":
        entrance(message)
    else:
        bot.send_message(message.chat.id, unexpected_message())
        main_menu(message)


@bot.message_handler(content_types=["text"])
def entrance(message):
    base = DB()
    connection = base.get_connection()
    user = User(connection)
    is_authorized = user.check_authorization(message.chat.id)
    if is_authorized:
        last_seen = is_authorized[0]
        last_try = is_authorized[1]
        authorization_time = check_time(last_seen)
        if authorization_time < 2592000:
            base.__del__()
            main_menu(message, "Чем я могу помочь?", True)
        else:
            base.__del__()
            bot.send_message(message.chat.id, "В целях безопасности, пожалуйста, пройдите авторизацию повторно")
            authorization_last_try(message, last_try, "start")
    else:
        start_menu(message)


if __name__ == "__main__":
    bot.polling(none_stop=True)
