import config
import telebot
from telebot import types
import datetime
from random import choice
from datetime import datetime
from time import sleep


def bot_greeting():
    welcome_messages = ['Привет!', 'Здравствуйте!', 'Приветствую Вас!', 'Ку!', 'Тевирп!', 'Хай!', 'daytime']
    greeting = choice(welcome_messages)
    if greeting == 'daytime':
        hours = int(str(datetime.now()).split()[1].split(':')[0])
        if hours < 12:
            greeting = '🌅Доброе утро!'
        elif 12 <= hours < 18:
            greeting = '🌈Добрый день!'
        else:
            greeting = '🌃Добрый вечер!'
    return greeting


def unexpected_message():
    error_messages = ['Я Вас не совсем понял(', 'Я не знаю, что с этим делать']
    message = choice(error_messages)
    return message


def farewell(bot, message):
    farewell_messages = ['👋До свидания!', '👋До встречи!']
    goodbye = choice(farewell_messages)
    bot.send_message(message.chat.id, goodbye)


def send_photo(bot, message, filename, caption_message=None):
    with open(filename, 'rb') as img:
        if caption_message:
            bot.send_photo(message.chat.id, img, caption=caption_message)
        else:
            bot.send_photo(message.chat.id, img)


def send_keyboard(bot, message, buttons, bot_message, one_time=False):
    if one_time:
        keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    else:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[types.KeyboardButton(name) for name in buttons])
    msg = bot.send_message(message.chat.id, bot_message, reply_markup=keyboard)
    return msg


def send_url_keyboard(bot, message, text, url, bot_message):
    url_keyboard = types.InlineKeyboardMarkup()
    url_keyboard.add(types.InlineKeyboardButton(text=text, url=url))
    bot.send_message(message.chat.id, bot_message, reply_markup=url_keyboard)


def check_time(last_time):
    now = int(datetime.today().timestamp())
    return now - last_time
