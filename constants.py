"""
auth_status has values:
not auth - if user is not authorized
auth in process - if user has sent his email to the bot
code wait - if the bot has sent the confirmation code to user's email
auth - confirmation code is right, user is authorized
"""

not_auth = "not_auth"
auth_in_process = "auth_in_process"
code_wait = "code_wait"
auth = "auth"
auth_status = "auth_status"

code = "code"
id = "id"
no_code = "Nan"
send = "send"
edit = "edit"
parse_mode = "HTML"
bot_emoji = "🤖"


# files
config_file = "config.json"
users_file = "users.json"
prof_file = "./Zayavlenie_priem_v_profsoyuz_student.pdf"
apos_file = "./Zayavlenie_APOS_edinorazovo.pdf"

# commands
start = "start"
text = "text"

# other text
sorry_txt = "Простите, но я не знаю, что на это ответить...\nВоспользуйтесь одной из команд или кнопок"
send_email_txt = "Отправьте пожалуйста вашу физтеховскую почту 📩"
hi_txt = "Здравствуйте! Я profkomBot 🤖\nСостоите ли вы в профсоюзе?"
union_txt = "Для работы со мной необходимо быть членом профсоюза!" \
            "\nЗаполните и пришлите на нашу почту profkom@phystech.edu"
sent_code_txt = "Я отправил на нее код с подтверждением. Пожалуйста, отправьте мне этот код 📬"
not_in_union_txt = "Упс, вы не состоите в профсоюзе"
not_email_txt = "Это не похоже на почту :O"
email_authorized_txt = "Вы подтвердили вашу почту ✅"

# callback data
begin = "begin"
in_union = "in labor union"
not_in_union = "not in labor union"

material_help = "material_help"
apos = "apos"
dispensary = "dispensary"
train = "train"
discounts = "discounts"
sos = "sos"

metro = "metro"
bonus = "bonus"
tele2 = "tele2"
skyeng = "skyeng"
clock = "clock"
x_fit = "x-fit"
boltay = "boltay"
theory = "theory"
schnitzel = "schnitzel"
herb_store = "herb-store"
driving_school = "driving_school"
buffet = "buffet"

phystech_email = "@phystech.edu"

# buttons' name
yes_name = "Да"
no_name = "Нет"
back_name = "⬅️Назад"
material_help_name = "Заявление на мат. помощь💰"
apos_name = "Заявление на АПОС💸"
dispensary_name = "Информация о профилактории🧖🏻‍♂️"
train_name = "Программа «РЖД бонус»🚂"
discounts_name = "Скидки и специальные предложения🤑"
sos_name = "Помощь🆘"

metro_name = "Карта METRO"
bonus_name = "РЖД бонус"
tele2_name = "Теле2"
skyeng_name = "SkyEng"
clock_name = "Циферблат"
x_fit_name = "X-fit Studio"
boltay_name = "кафе Boltay"
theory_name = "кафе Теория"
schnitzel_name = "Шницельная"
herb_store_name = "Магазин Herb-store.ru"
driving_school_name = "Автошкола"
buffet_name = "Буфет тройки"

# buttons' text
material_help_txt = "<a href='https://vk.cc/av1z3P'>Ссылка</a> на заявление на мат. помощь"
apos_txt = "Заполните заявление и пришлите на нашу почту profkom@phystech.edu\n\n" \
           "Или вы можете заполнить заявление в 224ГК\nВремя работы:\nПонедельник-пятница 09:30-16:30"
dispensary_txt = "https://telegra.ph/FAQ-po-profilaktoriyu-08-30"
train_txt = "<a href='https://vk.cc/8FFtFa'>Ссылка</a> на «РЖД бонус»"
sos_txt = "О возникших вопросах или проблемах пишите сюда:\n@dimicorn"
metro_txt = "Карта METRO\n\nОписание акции: Карта гостя работает 3 года.Наша карта: " \
            "Срок действия карты клиента METRO при условии хотя бы одной покупки в течение 12 месяцев неограничен. " \
            "В случае отсутствия покупок в указанный период METRO оставляет за собой право на ограничение доступа " \
            "в свои торговые центры. Также на ней копятся баллы и предоставляются скидки при оформлении\n\n " \
            "Как получить: https://vk.cc/8BhyW9"
bonus_txt = "РЖД бонус\n\nОписание акции: https://rzd-bonus.ru/about/student-program/\n\n" \
            "Как получить: https://vk.cc/8FFtFa"
tele2_txt = "Теле2\n\nОписание акции: Выгодные тарифы\n\nКак получить: https://www.mta-tele2.ru/"
skyeng_txt = "SkyEng\n\nОписание акции: Выгодные тарифы\n\nКак получить: https://corp.skyeng.ru/profkom-mfti"
clock_txt = "Циферблат\n\nОписание акции:  (https://vk.com/clokface)\n-20% с 10:00 до 19:00;\n" \
            "- 300 руб. за ночь (с 00:00 до 8:00)\n\nКак получить: Показать профсоюзный билет"
x_fit_txt = "X-fit Studio\n\nОписание акции: Абонемент на год - 10000 руб (-30%)\n на полгода - 7500 руб (-17%)\n" \
            "на месяц - 3000 руб (-40%)\n\nКак получить: Показать профсоюзный билет"
boltay_txt = "кафе Boltay\n\nОписание акции: Скидка 20% на все горячие напитки и воки для членов профсоюза " \
             "в «счастливые часы». А именно с 8:30 до 12:00 и с 19:00 до 00:00\n\n" \
             "Как получить: Показать профсоюзный билет"
theory_txt = "кафе Теория\n\nОписание акции: Скидка 10% на всё для членов профсоюза.\n\n " \
             "Как получить: Показать профсоюзный билет"
schnitzel_txt = "Шницельная\n\nОписание акции: Скидка 20% на всё для членов профсоюза.\n\n " \
                "Как получить: Показать профсоюзный билет"
herb_store_txt = "Магазин Herb-store.ru\n\nОписание акции: Скидка 10% на всё для членов профсоюза.\n\n" \
                 "Как получить: Показать профсоюзный билет"
driving_school_txt = "Автошкола\n\nОписание акции: Обучение для студентов МФТИ, заполнивших данную форму " \
                     "на категорию B стоит 30.000 при предъявлении студенческого билета, а на категорию A стоит " \
                     "15.000 (возможна рассрочка), и они получат специальный подарок от автошколы. Занятия по теории " \
                     "одинаковы для обеих категорий. Вождение у мото групп будет проходить на площадке в Мытищах, " \
                     "туда надо будет добраться самостоятельно.\n\n Как получить: https://forms.gle/QYqWQpPJ46FL5bQWA"
buffet_txt = "Буфет тройки\n\nОписание акции: Скидка 10% на всё для членов профсоюза.\n\n " \
             "Как получить: Показать профсоюзный билет"
discount_menu_txt = "Компании партнёры:"
start_menu_txt = "Сервисы и услуги:"

if __name__ == "__main__":
    print("You're running the wrong file!")
