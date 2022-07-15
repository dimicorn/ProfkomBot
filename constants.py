"""
auth_status has values:
not auth - if user is not authorized
auth in process - if user has sent his email to the bot
code wait - if the bot has sent the confirmation code to user's email
auth - confirmation code is right, user is authorized
"""
class Student:
    id = 0
    auth_status = not_auth
    code = no_code

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
files = {"bonus_config"      : "configs/bonus_config.json", 
         "profkomlist_config": "configs/profkomlist_config.json",
         "config"            : "configs/config.json",
         "users"             : "data/users.json",
         "profkom_card"      : "data/profkom_card"}


# commands
start = "start"
text = "text"

# other text
txts = { \
    "sorry"            : "Простите, но я не знаю, что на это ответить...\nВоспользуйтесь одной из команд или кнопок",
    "send_email"       : "Отправьте пожалуйста вашу физтеховскую почту ",
    "hi"               : "Здравствуйте! Я profkomBot 🤖\nСостоите ли вы в профсоюзе??",
    "union"            : "Для работы со мной необходимо быть членом профсоюза!\nЗаполните <a href='https://vk.com/doc299776632_583719520?hash=798af086b55ca296b4&dl=1339ce4781f7e18eff' download='newfilename'>заявление</a> и пришлите на нашу почту profkom@phystech.edu",
    "sent_code"        : "Я отправил на нее код с подтверждением. Пожалуйста, отправьте мне этот код",
    "not_in_union"     : "Упс, вы не состоите в профсоюзе",
    "not_email"        : "Это не похоже на почту :O",
    "email_authorized" : "Вы подтвердили вашу почту ✅",
    "material_help"    : "<a href='https://vk.cc/av1z3P'>Ссылка</a> на заявление на мат. помощь",
    "apos"             : "Заполните <a href='https://mipt.ru/profkom/students/soc_scolarship/Zayavlenie_APOS_edinorazovo.pdf'>заявление</a> и пришлите на нашу почту profkom@phystech.edu\n\n Или вы можете заполнить заявление в 224ГК\nВремя работы:\nПонедельник-пятница 09:30-16:30",
    "dispensary"       : "https://telegra.ph/FAQ-po-profilaktoriyu-08-30",
    "sos"              : "О возникших вопросах или проблемах пишите сюда:\n@dimicorn",
    "discount_menu"    : "Компании партнёры:",
    "start_menu"       : "Сервисы и услуги:"}

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
if __name__ == "__main__":
    print("You're running the wrong file!")
