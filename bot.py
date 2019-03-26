import config
import telebot
from telebot import types
from random import choice
from datetime import datetime
from bot_functions import services, feedback, navigation, privileges, bot_help

bot = telebot.TeleBot(config.token)


def farewell(message):
    farewell_messages = ['До свидания!', 'До встречи!']
    goodbye = choice(farewell_messages)
    bot.send_message(message.chat.id, goodbye)


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
    keyboard.add(*[types.InlineKeyboardButton(text=name, callback_data='start_{}'.format(name)) for name in ['Да',
                                                                                                             'Нет']])
    bot.send_message(message.chat.id, "Я могу Вам помочь?", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda button: 'start' in button.data and True)
def keyboard_answer(button):
    msg = button.message
    if button.data.split('_')[1] == 'Да':
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
        short_history(m)
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


def last_message(message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*[types.InlineKeyboardButton(text=name, callback_data='last_{}'.format(name)) for name in ['Да',
                                                                                                            'Нет']])
    bot.send_message(message.chat.id, "Вам еще нужна помощь?", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda button: 'last' in button.data and True)
def last_message_answer(button):
    if button.data.split('_')[1] == 'Да':
        main_menu(button.message)
    else:
        farewell(button.message)


@bot.message_handler(commands=["history", "история"])
def short_history(message):
    bot.send_message(message.chat.id, '*short history*')
    start_history(message)


def start_history(message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*[types.InlineKeyboardButton(text=name, callback_data='history1_{}'.format(name)) for name in ['Да',
                                                                                                                'Нет']])
    bot.send_message(message.chat.id, 'Хотите узнать больше?', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda button: 'history1' in button.data and True)
def start_history_answer(button):
    if button.data.split('_')[1] == 'Да':
        short_history_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        short_history_keyboard.add(*[types.KeyboardButton(name) for name in ['History№1', 'History№2', 'History№3',
                                                                             'Меню']])
        msg = bot.send_message(button.message.chat.id, "О чём хотите узнать?", reply_markup=short_history_keyboard)
        bot.register_next_step_handler(msg, history)
    else:
        last_message(button.message)


def history(m):
    if m.text == 'Меню':
        main_menu(m)
    else:
        bot.send_message(m.chat.id, config.histories[m.text])
        start_history(m)


if __name__ == '__main__':
    bot.polling(none_stop=True)

