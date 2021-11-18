import telebot
from telebot import types
from config import token
import backend
import database

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    if database.check_verification(message) == False:
        bot.send_message(message.chat.id, "Добро пожаловать! Для начала вам нужно пройти верификацию.", reply_markup=verification())
    else:
        text = 'Вы уже верифицированы и можете узнать количество посещений'
        bot.send_message(message.chat.id, text, reply_markup=check_visits())


@bot.message_handler(content_types=["text"])
def send_text(message):
    if message.text == 'Пройти верификацию':
        verificate(message)

    elif message.text == 'Узнать количество посещений':
        text = database.get_visits(message)
        bot.send_message(message.chat.id, text, reply_markup=check_visits())

def verificate(message):
    if database.check_ban(message) == False:
        text = 'Введите вашу почту @phystech.edu'
        bot.send_message(message.chat.id, text)
        bot.register_next_step_handler(message, check_email)
    else:
        text = f'К сожалению, вы пока не можете пройти верификацию.\n\n\nОсталось ждать {database.check_ban(message)}'
        bot.send_message(message.chat.id, text, reply_markup=verification())
        bot.register_next_step_handler(message, verificate)

def check_email(message):
    text = backend.check_email(message)
    if text == 'Вы указали неверную почту':
        bot.send_message(message.chat.id, text)
        text = 'Введите вашу почту @phystech.edu'
        bot.send_message(message.chat.id, text)
        bot.register_next_step_handler(message, check_email)
    else:
        bot.send_message(message.chat.id, text)
        bot.register_next_step_handler(message, enter_code)


def enter_code(message):
    code = message.text
    text = backend.check_code(message, code)
    if text == 'Вы прошли верификацию':
        bot.send_message(message.chat.id, text, reply_markup=check_visits())
    elif text == 'Вы ввели неправильный код :(\n\nПопробуйте еще раз!':
        result = database.add_attempt(message)
        if result == True:
            bot.send_message(message.chat.id, text)
            bot.register_next_step_handler(message, enter_code)
        else:
            text = 'К сожалению, вы 3 раза ввели неправильный код. Повторите попытку через 24 часа'
            bot.send_message(message.chat.id, text, reply_markup=verification())


@bot.callback_query_handler(func=lambda message: True)
def verification():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.KeyboardButton('Пройти верификацию')
    markup.add(btn1)
    return markup

def check_visits():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Узнать количество посещений')
    markup.add(btn1)
    return markup


bot.polling(none_stop=True)
