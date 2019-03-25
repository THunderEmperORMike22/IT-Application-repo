import config
import telebot
from telebot import types
from random import choice
from datetime import datetime
from bot_functions import farewell, services, history, feedback, navigation, privileges, bot_help
# from Bot_history import history


bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=["start"])
def start_message(message):
    welcome_messages = ['Привет!', 'Здравствуйте!', 'Приветствую Вас!', 'daytime']
    greeting = choice(welcome_messages)
    if greeting == 'daytime':
        hours = int(str(datetime.now()).split()[1].split(':')[0])
        if hours < 12:
            greeting = 'Доброе утро!'
        elif 12 <= hours < 18:
            greeting = 'Добрый день!'
        else:
            greeting = 'Добрый вечер!'
    bot.send_message(message.chat.id, greeting)
    bot.send_message(message.chat.id, config.description)
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in ['Да', 'Нет']])
    bot.send_message(message.chat.id, "Я могу Вам помочь?", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda button: True)
def keyboard_answer(button):
    msg = button.message
    if button.data == 'Да':
        main_menu(msg)
    else:
        farewell(msg)


@bot.message_handler(commands=['menu'])
def main_menu(message):
    menu_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    menu_keyboard.add(*[types.KeyboardButton(name) for name in ['История', 'Сервисы', 'Привилегии',
                                                                'Навигация', 'Обратная связь', 'Помощь']])
    msg = bot.send_message(message.chat.id, "Чем я могу помочь?", reply_markup=menu_keyboard)
    bot.register_next_step_handler(msg, menu_functions)


def menu_functions(m):
    if m.text == 'История':
        history(m, 'Хотите узнать об истории компании?')
    elif m.text == 'Сервисы':
        services(m.chat.id)
    elif m.text == 'Привилегии':
        privileges(m.chat.id)
    elif m.text == 'Навигация':
        navigation(m.chat.id)
    elif m.text == 'Обратная связь':
        feedback(m.chat.id)
    elif m.text == 'Помощь':
        bot_help(m.chat.id)


'''@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    bot.send_message(message.chat.id, message.text)
'''

if __name__ == '__main__':
    bot.polling(none_stop=True)

