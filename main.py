import telebot
from telebot import types
import json
import EmailSender
import time
import GoogleSheets as gs

"""
auth_status has values:
not auth - if user is not authorized
auth in process - if user has sent his email to the bot
code wait - if the bot has sent the confirmation code to user's email
auth - confirmation code is right, user is authorized
"""


def start_menu(bot, message, view):
    markup = types.InlineKeyboardMarkup(row_width=1)
    # inline buttons
    item1 = types.InlineKeyboardButton("Заявление на мат. помощь💰", callback_data="material help")
    item2 = types.InlineKeyboardButton("Заявление на АПОС💸", callback_data="apos")
    item3 = types.InlineKeyboardButton("Информация о профилактории🧖🏻‍♂️", callback_data="dispensary")
    item4 = types.InlineKeyboardButton("Программа «РЖД бонус»🚂", callback_data="train")
    item5 = types.InlineKeyboardButton("Скидки и специальные предложения🤑", callback_data="discounts")
    item6 = types.InlineKeyboardButton("Помощь🆘", callback_data="help")
    items = [item1, item2, item3, item4, item5, item6]
    for i in items:
        markup.row(i)
    if view == "send":
        bot.send_message(message.chat.id, "Сервисы и услуги:", reply_markup=markup)
    elif view == "edit":
        bot.edit_message_text(chat_id=message.chat.id, text="Сервисы и услуги:", reply_markup=markup,
                              message_id=message.message_id, )


# random code generator
def rand(x):
    hour = x.tm_hour
    mins = x.tm_min
    sec = x.tm_sec
    hour = hour * 3600
    mins = mins * 60
    t = hour + mins + sec
    return t


def main():
    with open("config.json") as a:
        config = json.load(a)
    a.close()

    token = config["token"]
    bot = telebot.TeleBot(token)

    # defining /start command
    @bot.message_handler(commands=["start"])
    def welcome(message):
        # loading all authorized users
        with open("users.json") as f:
            users = json.load(f)
        f.close()

        if str(message.from_user.id) in users and users[str(message.from_user.id)]["auth_status"] == "auth":
            # user is not first time using bot and is authorized
            # bot.send_message(message.chat.id, "Я профкомБот🤖\nЖду ваших команд!"
            start_menu(bot, message, "send")
        else:  # user is not authorized/first time using the bot
            users[message.from_user.id] = \
                {"id": message.from_user.id, "auth_status": "not auth", "code": "Nan"}
            markup = types.InlineKeyboardMarkup(row_width=2)
            # inline buttons
            item1 = types.InlineKeyboardButton("Да", callback_data="in labor union")
            item2 = types.InlineKeyboardButton("Нет", callback_data="not in labor union")
            markup.row(item1, item2)
            bot.send_message(message.chat.id,
                             "Здравствуйте! Я profkomBot 🤖\nСостоите ли вы в профсоюзе?", reply_markup=markup)
            # updating users.json
            users_file = open("users.json", "w")
            json.dump(users, users_file)
            users_file.close()

    '''
    # defining /services command
    @bot.message_handler(commands=["services"])
    def service(message):
        # loading users
        with open("users.json") as f:
            users = json.load(f)
        f.close()

        if users[str(message.from_user.id)]["auth_status"] == "auth":  # only authorized users has access to the command

        else:
            bot.send_message(message.chat.id,
                             "Простите, но я не знаю, что на это ответить...\n"
                             "Воспользуйтесь одной из команд или кнопок")
    '''

    # defining messages to the bot
    @bot.message_handler(content_types=["text"])
    def echo(message):
        # loading users
        with open("users.json") as f:
            users = json.load(f)
        f.close()

        if users[str(message.from_user.id)]["auth_status"] == "auth in process":
            email = message.text
            if email[-13:] == "@phystech.edu":  # checking if it's a phystech email
                if gs.find_user(email):  # checking if it is in labor union table
                    bot.send_message(message.chat.id,
                                     "Я отправил на нее код с подтверждением. "
                                     "Пожалуйста, отправьте мне этот код 📬")
                    # generating confirmation code
                    temp = time.gmtime()
                    code = rand(temp)
                    # sending confirmation code to the user
                    EmailSender.send_email(email, code)

                    users[str(message.from_user.id)]["auth_status"] = "code wait"
                    users[str(message.from_user.id)]["code"] = code
                    # updating users.json
                    users_file = open("users.json", "w")
                    json.dump(users, users_file)
                    users_file.close()

                else:
                    bot.send_message(message.chat.id, "Упс, вы не состоите в профсоюзе")
                    users[str(message.from_user.id)]["auth_status"] = "not auth"
                    # updating users.json
                    users_file = open("users.json", "w")
                    json.dump(users, users_file)
                    users_file.close()
            else:
                bot.send_message(message.chat.id, "Это не похоже на почту :O")

        elif users[str(message.from_user.id)]["auth_status"] == "code wait":
            key = message.text
            if key == str(users[str(message.from_user.id)]["code"]):
                # checking in the user texted the right confirmation code from the email
                bot.send_message(message.chat.id, "Вы подтвердили вашу почту ✅")
                start_menu(bot, message, "send")
                users[str(message.from_user.id)]["auth_status"] = "auth"
                # updating users.json
                users_file = open("users.json", "w")
                json.dump(users, users_file)
                users_file.close()
            else:
                bot.send_message(message.chat.id, "Код " + key + " неверный ❌\nНапишите код из письма")
                users[str(message.from_user.id)]["auth_status"] = "code wait"
                # updating users.json
                users_file = open("users.json", "w")
                json.dump(users, users_file)
                users_file.close()
        else:
            bot.send_message(message.chat.id,
                             "Простите, но я не знаю, что на это ответить...\n"
                             "Воспользуйтесь одной из команд или кнопок")

    # buttons interaction
    @bot.callback_query_handler(func=lambda call: True)
    def callback_inline(call):
        # loading users
        with open("users.json") as f:
            users = json.load(f)
        try:
            if call.message:
                bot.answer_callback_query(call.id, show_alert=False, text="🤖")
                if call.data == "in labor union":
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                          text="Отправьте пожалуйста вашу физтеховскую почту 📩")
                    users[str(call.message.chat.id)]["auth_status"] = "auth in process"
                    # updating users.json
                    users_file = open("users.json", "w")
                    json.dump(users, users_file)
                    users_file.close()
                elif call.data == "not in labor union":
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                          text="Для работы со мной необходимо быть членом профсоюза!"
                                               "\nЗаполните и пришлите на нашу почту profkom@phystech.edu")
                    doc = open("./Zayavlenie_priem_v_profsoyuz_student.pdf", "rb")
                    bot.send_document(call.message.chat.id, doc)
                if users[str(call.message.chat.id)]["auth_status"] == "auth":
                    if call.data == "begin":
                        start_menu(bot, call.message, "edit")
                    elif call.data == "material help":
                        markup = types.InlineKeyboardMarkup(row_width=1)
                        back = types.InlineKeyboardButton("⬅️Назад", callback_data="begin")
                        markup.row(back)
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                              text="<a href='https://vk.cc/av1z3P'>Ссылка</a> "
                                                   "на заявление на мат. помощь", parse_mode="HTML",
                                              reply_markup=markup)
                    elif call.data == "apos":
                        markup = types.InlineKeyboardMarkup(row_width=1)
                        back = types.InlineKeyboardButton("⬅️Назад", callback_data="begin")
                        markup.row(back)
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                              text="Заполните заявление"
                                                   " и пришлите на нашу почту profkom@phystech.edu\n\n"
                                                   "Или вы можете заполнить заявление в 224ГК\nВремя работы:\n"
                                                   "Понедельник-пятница 09:30-16:30", parse_mode="HTML",
                                              reply_markup=markup)
                        doc = open("./Zayavlenie_APOS_edinorazovo.pdf", "rb")
                        bot.send_document(call.message.chat.id, doc)
                    elif call.data == "dispensary":
                        markup = types.InlineKeyboardMarkup(row_width=1)
                        back = types.InlineKeyboardButton("⬅️Назад", callback_data="begin")
                        markup.row(back)
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                              text="https://telegra.ph/FAQ-po-profilaktoriyu-08-30",
                                              reply_markup=markup)
                    elif call.data == "train":
                        markup = types.InlineKeyboardMarkup(row_width=1)
                        back = types.InlineKeyboardButton("⬅️Назад", callback_data="begin")
                        markup.row(back)
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                              text="<a href='https://vk.cc/8FFtFa'>Ссылка</a> на «РЖД бонус»",
                                              parse_mode="HTML", reply_markup=markup)
                    elif call.data == "discounts":
                        markup = types.InlineKeyboardMarkup(row_width=1)
                        # inline buttons
                        item1 = types.InlineKeyboardButton("Карта METRO", callback_data="metro")
                        item2 = types.InlineKeyboardButton("РЖД бонус", callback_data="bonus")
                        item3 = types.InlineKeyboardButton("Теле2", callback_data="tele2")
                        item4 = types.InlineKeyboardButton("SkyEng", callback_data="skyeng")
                        item5 = types.InlineKeyboardButton("Циферблат", callback_data="clock")
                        item6 = types.InlineKeyboardButton("X-fit Studio", callback_data="x-fit")
                        item7 = types.InlineKeyboardButton("кафе Boltay", callback_data="boltay")
                        item8 = types.InlineKeyboardButton("кафе Теория", callback_data="theory")
                        item9 = types.InlineKeyboardButton("Шницельная", callback_data="schnitzel")
                        item10 = types.InlineKeyboardButton("Магазин Herb-store.ru", callback_data="herb-store")
                        item11 = types.InlineKeyboardButton("Автошкола", callback_data="driving school")
                        item12 = types.InlineKeyboardButton("Буфет тройки", callback_data="buffet")
                        item13 = types.InlineKeyboardButton("⬅️Назад", callback_data="begin")
                        items = [item1, item2, item3, item4, item5, item6, item7, item8, item9, item10, item11, item12,
                                 item13]
                        for i in range(0, len(items) - 1, 2):
                            markup.row(items[i], items[i + 1])
                        markup.row(item13)
                        bot.edit_message_text(chat_id=call.message.chat.id, text="Компании партнёры:",
                                              message_id=call.message.message_id, reply_markup=markup)
                    elif call.data == "help":
                        markup = types.InlineKeyboardMarkup(row_width=1)
                        back = types.InlineKeyboardButton("⬅️Назад", callback_data="begin")
                        markup.row(back)
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                              text="О возникших вопросах или проблемах пишите сюда:\n@dimicorn",
                                              reply_markup=markup)
                    elif call.data == "metro":
                        markup = types.InlineKeyboardMarkup(row_width=1)
                        back = types.InlineKeyboardButton("⬅️Назад", callback_data="discounts")
                        markup.row(back)
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                              text="Карта METRO\n\nОписание акции: Карта гостя работает 3 года.Наша "
                                                   "карта: Срок "
                                                   "действия карты клиента METRO при условии хотя бы одной покупки в "
                                                   "течение "
                                                   "12 месяцев неограничен. В случае отсутствия покупок в указанный "
                                                   "период METRO "
                                                   "оставляет за собой право на ограничение доступа в свои торговые "
                                                   "центры. "
                                                   "Также на ней копятся баллы и предоставляются скидки при "
                                                   "оформлении\n\n "
                                                   "Как получить: https://vk.cc/8BhyW9", reply_markup=markup)
                    elif call.data == "bonus":
                        markup = types.InlineKeyboardMarkup(row_width=1)
                        back = types.InlineKeyboardButton("⬅️Назад", callback_data="discounts")
                        markup.row(back)
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                              text="РЖД бонус\n\n"
                                                   "Описание акции: https://rzd-bonus.ru/about/student-program/\n\n"
                                                   "Как получить: https://vk.cc/8FFtFa", reply_markup=markup)
                    elif call.data == "tele2":
                        markup = types.InlineKeyboardMarkup(row_width=1)
                        back = types.InlineKeyboardButton("⬅️Назад", callback_data="discounts")
                        markup.row(back)
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                              text="Теле2\n\nОписание акции: Выгодные тарифы\n\n"
                                                   "Как получить: https://www.mta-tele2.ru/", reply_markup=markup)
                    elif call.data == "skyeng":
                        markup = types.InlineKeyboardMarkup(row_width=1)
                        back = types.InlineKeyboardButton("⬅️Назад", callback_data="discounts")
                        markup.row(back)
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                              text="SkyEng\n\nОписание акции: Выгодные тарифы\n\n"
                                                   "Как получить: https://corp.skyeng.ru/profkom-mfti",
                                              reply_markup=markup)
                    elif call.data == "clock":
                        markup = types.InlineKeyboardMarkup(row_width=1)
                        back = types.InlineKeyboardButton("⬅️Назад", callback_data="discounts")
                        markup.row(back)
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                              text="Циферблат\n\nОписание акции:  (https://vk.com/clokface)\n"
                                                   "-20% с 10:00 до 19:00;\n- 300 руб. за ночь (с 00:00 до 8:00)\n\n"
                                                   "Как получить: Показать профсоюзный билет", reply_markup=markup)
                    elif call.data == "x-fit":
                        markup = types.InlineKeyboardMarkup(row_width=1)
                        back = types.InlineKeyboardButton("⬅️Назад", callback_data="discounts")
                        markup.row(back)
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                              text="X-fit Studio\n\nОписание акции: Абонемент на год - 10000 руб ("
                                                   "-30%)\n "
                                                   "на полгода - 7500 руб (-17%)\nна месяц - 3000 руб (-40%)\n\n"
                                                   "Как получить: Показать профсоюзный билет", reply_markup=markup)
                    elif call.data == "boltay":
                        markup = types.InlineKeyboardMarkup(row_width=1)
                        back = types.InlineKeyboardButton("⬅️Назад", callback_data="discounts")
                        markup.row(back)
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                              text="кафе Boltay\n\nОписание акции: Скидка 20% на все горячие "
                                                   "напитки и воки для членов профсоюза в «счастливые часы». "
                                                   "А именно с 8:30 до 12:00 и с 19:00 до 00:00\n\n"
                                                   "Как получить: Показать профсоюзный билет", reply_markup=markup)
                    elif call.data == "theory":
                        markup = types.InlineKeyboardMarkup(row_width=1)
                        back = types.InlineKeyboardButton("⬅️Назад", callback_data="discounts")
                        markup.row(back)
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                              text="кафе Теория\n\nОписание акции: Скидка 10% на всё для членов "
                                                   "профсоюза.\n\n "
                                                   "Как получить: Показать профсоюзный билет", reply_markup=markup)
                    elif call.data == "schnitzel":
                        markup = types.InlineKeyboardMarkup(row_width=1)
                        back = types.InlineKeyboardButton("⬅️Назад", callback_data="discounts")
                        markup.row(back)
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                              text="Шницельная\n\nОписание акции: Скидка 20% на всё для членов "
                                                   "профсоюза.\n\n "
                                                   "Как получить: Показать профсоюзный билет", reply_markup=markup)
                    elif call.data == "herb-store":
                        markup = types.InlineKeyboardMarkup(row_width=1)
                        back = types.InlineKeyboardButton("⬅️Назад", callback_data="discounts")
                        markup.row(back)
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                              text="Магазин Herb-store.ru\n\nОписание акции: "
                                                   "Скидка 10% на всё для членов профсоюза.\n\n"
                                                   "Как получить: Показать профсоюзный билет", reply_markup=markup)
                    elif call.data == "driving school":
                        markup = types.InlineKeyboardMarkup(row_width=1)
                        back = types.InlineKeyboardButton("⬅️Назад", callback_data="discounts")
                        markup.row(back)
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                              text="Автошкола\n\nОписание акции: Обучение для студентов МФТИ, "
                                                   "заполнивших данную форму на категорию B стоит 30.000 при "
                                                   "предъявлении "
                                                   "студенческого билета, а на категорию A стоит 15.000 (возможна "
                                                   "рассрочка), "
                                                   "и они получат специальный подарок от автошколы. Занятия по теории "
                                                   "одинаковы "
                                                   "для обеих категорий. Вождение у мото групп будет проходить "
                                                   "на площадке в Мытищах, туда надо будет добраться "
                                                   "самостоятельно.\n\n "
                                                   "Как получить: https://forms.gle/QYqWQpPJ46FL5bQWA",
                                              reply_markup=markup)
                    elif call.data == "buffet":
                        markup = types.InlineKeyboardMarkup(row_width=1)
                        back = types.InlineKeyboardButton("⬅️Назад", callback_data="discounts")
                        markup.row(back)
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                              text="Буфет тройки\n\nОписание акции: Скидка 10% на всё для членов "
                                                   "профсоюза.\n\n "
                                                   "Как получить: Показать профсоюзный билет", reply_markup=markup)
        except Exception as e:
            print(repr(e))

    # run
    bot.polling(none_stop=True)


if __name__ == "__main__":
    main()
