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
            '''
            if :  # user is authorized
                bot.send_message(message.chat.id, "Я профкомБот🤖\nЖду ваших команд!")
            else:
                markup = types.InlineKeyboardMarkup(row_width=2)
                # inline buttons
                item1 = types.InlineKeyboardButton("Да", callback_data='in labor union')
                item2 = types.InlineKeyboardButton("Нет", callback_data='not in labor union')
                markup.row(item1, item2)
                bot.send_message(message.chat.id,
                                 "Здравствуйте! Я profkomBot 🤖\nСостоите ли вы в профсоюзе?", reply_markup=markup)
            '''
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

    # defining /services command
    @bot.message_handler(commands=["services"])
    def service(message):
        # loading users
        with open("users.json") as f:
            users = json.load(f)
        f.close()

        if users[str(message.from_user.id)]["auth_status"] == "auth":  # only authorized users has access to the command
            markup = types.InlineKeyboardMarkup(row_width=1)
            # inline buttons
            item1 = types.InlineKeyboardButton("Заявление на мат. помощь💰", callback_data="material help")
            item2 = types.InlineKeyboardButton("Заявление на АПОС💸", callback_data="apos")
            item3 = types.InlineKeyboardButton("Информация о профилактории🧖🏻‍♂️", callback_data="dispensary")
            item4 = types.InlineKeyboardButton("Программа «РЖД бонус»🚂", callback_data="train")
            item5 = types.InlineKeyboardButton("Вступление в профсоюз📋", callback_data="labor union")
            item6 = types.InlineKeyboardButton("Скидки и специальные предложения🤑", callback_data="discounts")
            item7 = types.InlineKeyboardButton("Помощь🆘", callback_data="help")
            items = [item1, item2, item3, item4, item5, item6, item7]
            for i in items:
                markup.row(i)
            bot.send_message(message.chat.id, "Сервисы и услуги:", reply_markup=markup)
        else:
            bot.send_message(message.chat.id,
                             "Простите, но я не знаю, что на это ответить...\n"
                             "Воспользуйтесь одной из команд или кнопок")

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
                    bot.send_message(call.message.chat.id, "Отправьте пожалуйста вашу физтеховскую почту 📩")
                    users[str(call.message.chat.id)]["auth_status"] = "auth in process"
                    # updating users.json
                    users_file = open("users.json", "w")
                    json.dump(users, users_file)
                    users_file.close()
                elif call.data == "not in labor union":
                    bot.send_message(call.message.chat.id,
                                     "Для работы со мной необходимо быть членом профсоюза!"
                                     "\nЗаполните и пришлите на нашу почту profkom@phystech.edu")
                    doc = open("./Zayavlenie_priem_v_profsoyuz_student.pdf", "rb")
                    bot.send_document(call.message.chat.id, doc)
                if users[str(call.message.chat.id)]["auth_status"] == "auth":
                    if call.data == "material help":
                        bot.send_message(call.message.chat.id,
                                         "Ссылка на заявление на мат. помощь:\n https://vk.cc/av1z3P")
                    elif call.data == "apos":
                        bot.send_message(call.message.chat.id,
                                         "Заполните и пришлите на нашу почту\nprofkom@phystech.edu\n\n"
                                         "Ссылка на заявление: https://vk.cc/c5v2DV")
                        bot.send_message(call.message.chat.id,
                                         "Или вы можете заполнить заявление в 224ГК\n\nВремя работы:\n"
                                         "Понедельник-пятница 09:30-16:30")
                    elif call.data == "dispensary":
                        bot.send_message(call.message.chat.id, "https://telegra.ph/FAQ-po-profilaktoriyu-08-30")
                    elif call.data == "train":
                        bot.send_message(call.message.chat.id, "Ссылка на «РЖД бонус»:\nhttps://vk.cc/8FFtFa")
                    elif call.data == "labor union":
                        doc = open("./Zayavlenie_priem_v_profsoyuz_student.pdf", "rb")
                        bot.send_document(call.message.chat.id, doc)
                        bot.send_message(call.message.chat.id,
                                         "Заполните и пришлите на нашу почту\nprofkom@phystech.edu")
                    elif call.data == "discounts":
                        markup = types.InlineKeyboardMarkup(row_width=1)
                        # inline buttons
                        item1 = types.InlineKeyboardButton("Карта Metro", callback_data="metro")
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
                        items = [item1, item2, item3, item4, item5, item6, item7, item8, item9, item10, item11, item12]
                        for i in items:
                            markup.row(i)
                        bot.send_message(call.message.chat.id, "Компании партнёры:", reply_markup=markup)
                    elif call.data == "help":
                        bot.send_message(call.message.chat.id,
                                         "О возникших вопросах или проблемах пишите сюда:\n@dimicorn")
                    elif call.data == "metro":
                        bot.send_message(call.message.chat.id,
                                         "Карта Metro\n\nОписание акции: Карта гостя работает 3 года.Наша карта: Срок "
                                         "действия карты клиента METRO при условии хотя бы одной покупки в течение "
                                         "12 месяцев неограничен. В случае отсутствия покупок в указанный период METRO "
                                         "оставляет за собой право на ограничение доступа в свои торговые центры. "
                                         "Также на ней копятся баллы и предоставляются скидки при оформлении\n\n"
                                         "Как получить: https://vk.cc/8BhyW9")
                    elif call.data == "bonus":
                        bot.send_message(call.message.chat.id,
                                         "РЖД бонус\n\n"
                                         "Описание акции: https://rzd-bonus.ru/about/student-program/\n\n"
                                         "Как получить: https://vk.cc/8FFtFa")
                    elif call.data == "tele2":
                        bot.send_message(call.message.chat.id,
                                         "Теле2\n\nОписание акции: Выгодные тарифы\n\n"
                                         "Как получить: https://www.mta-tele2.ru/")
                    elif call.data == "skyeng":
                        bot.send_message(call.message.chat.id,
                                         "SkyEng\n\nОписание акции: Выгодные тарифы\n\n"
                                         "Как получить: https://corp.skyeng.ru/profkom-mfti")
                    elif call.data == "clock":
                        bot.send_message(call.message.chat.id,
                                         "Циферблат\n\nОписание акции:  (https://vk.com/clokface)\n"
                                         "-20% с 10:00 до 19:00;\n- 300 руб. за ночь (с 00:00 до 8:00)\n\n"
                                         "Как получить: Показать профсоюзный билет")
                    elif call.data == "x-fit":
                        bot.send_message(call.message.chat.id,
                                         "X-fit Studio\n\nОписание акции: Абонемент на год - 10000 руб (-30%)\n"
                                         "на полгода - 7500 руб (-17%)\nна месяц - 3000 руб (-40%)\n\n"
                                         "Как получить: Показать профсоюзный билет")
                    elif call.data == "boltay":
                        bot.send_message(call.message.chat.id,
                                         "кафе Boltay\n\nОписание акции: Скидка 20% на все горячие "
                                         "напитки и воки для членов профсоюза в «счастливые часы». "
                                         "А именно с 8:30 до 12:00 и с 19:00 до 00:00\n\n"
                                         "Как получить: Показать профсоюзный билет")
                    elif call.data == "theory":
                        bot.send_message(call.message.chat.id,
                                         "кафе Теория\n\nОписание акции: Скидка 10% на всё для членов профсоюза.\n\n"
                                         "Как получить: Показать профсоюзный билет")
                    elif call.data == "schnitzel":
                        bot.send_message(call.message.chat.id,
                                         "Шницельная\n\nОписание акции: Скидка 20% на всё для членов профсоюза.\n\n"
                                         "Как получить: Показать профсоюзный билет")
                    elif call.data == "herb-store":
                        bot.send_message(call.message.chat.id,
                                         "Магазин Herb-store.ru\n\nОписание акции: "
                                         "Скидка 10% на всё для членов профсоюза.\n\n"
                                         "Как получить: Показать профсоюзный билет")
                    elif call.data == "driving school":
                        bot.send_message(call.message.chat.id,
                                         "Автошкола\n\nОписание акции: Обучение для студентов МФТИ, "
                                         "заполнивших данную форму на категорию B стоит 30.000 при предъявлении "
                                         "студенческого билета, а на категорию A стоит 15.000 (возможна рассрочка), "
                                         "и они получат специальный подарок от автошколы. Занятия по теории одинаковы "
                                         "для обеих категорий. Вождение у мото групп будет проходить "
                                         "на площадке в Мытищах, туда надо будет добраться самостоятельно.\n\n"
                                         "Как получить: https://forms.gle/QYqWQpPJ46FL5bQWA")
                    elif call.data == "buffet":
                        bot.send_message(call.message.chat.id,
                                         "Буфет тройки\n\nОписание акции: Скидка 10% на всё для членов профсоюза.\n\n"
                                         "Как получить: Показать профсоюзный билет")
        except Exception as e:
            print(repr(e))

    # run
    bot.polling(none_stop=True)


if __name__ == "__main__":
    main()
