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
files = {"bonus_config": "configs/bonus_config.json", 
         "profkomlist_config": "configs/profkomlist_config.json",
         "config": "configs/config.json"}


config_file = "configs/config.json"
users_file = "users.json"
prof_file = "data/Zayavlenie_priem_v_profsoyuz_student.pdf"
apos_file = "data/Zayavlenie_APOS_edinorazovo.pdf"

# commands
start = "start"
text = "text"

# other text
sorry_txt = "Простите, но я не знаю, что на это ответить...\nВоспользуйтесь одной из команд или кнопок"
send_email_txt = "Отправьте пожалуйста вашу физтеховскую почту 📩"
hi_txt = "Здравствуйте! Я profkomBot 🤖\nСостоите ли вы в профсоюзе?"
union_txt = "Для работы со мной необходимо быть членом профсоюза!" \
        "\nЗаполните <a href='https://vk.com/doc299776632_583719520?hash=798af086b55ca296b4&dl=1339ce4781f7e18eff' download='newfilename'>заявление</a> и пришлите на нашу почту profkom@phystech.edu"
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
discounts = "discounts"
sos = "sos"

phystech_email = "@phystech.edu"

# buttons' name
yes_name = "Да"
no_name = "Нет"
back_name = "⬅️Назад"
material_help_name = "Заявление на мат. помощь💰"
apos_name = "Заявление на АПОС💸"
dispensary_name = "Информация о профилактории🧖🏻‍♂️"
discounts_name = "Скидки и специальные предложения🤑"
sos_name = "Помощь🆘"


# buttons' text
material_help_txt = "<a href='https://vk.cc/av1z3P'>Ссылка</a> на заявление на мат. помощь"
apos_txt = "Заполните <a href='https://mipt.ru/profkom/students/soc_scolarship/Zayavlenie_APOS_edinorazovo.pdf'>заявление</a> и пришлите на нашу почту profkom@phystech.edu\n\n" \
           "Или вы можете заполнить заявление в 224ГК\nВремя работы:\nПонедельник-пятница 09:30-16:30"
dispensary_txt = "https://telegra.ph/FAQ-po-profilaktoriyu-08-30"
sos_txt = "О возникших вопросах или проблемах пишите сюда:\n@dimicorn"
discount_menu_txt = "Компании партнёры:"
start_menu_txt = "Сервисы и услуги:"

if __name__ == "__main__":
    print("You're running the wrong file!")
