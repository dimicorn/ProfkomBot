import EmailSender
import GoogleSheets as gs
import time
import json
from telebot import types
import constants as const
from datetime import date

# random code generator
def rand(x):
    hour = x.tm_hour
    mins = x.tm_min
    sec = x.tm_sec
    hour = hour * 3600
    mins = mins * 60
    t = hour + mins + sec
    return t


def users_file_load():
    with open(const.users_file) as f:
        users = json.load(f)
    f.close()
    return users


def users_file_dump(users):
    users_file = open(const.users_file, "w")
    json.dump(users, users_file)
    users_file.close()


def start_menu(bot, message, view):
    markup = types.InlineKeyboardMarkup(row_width=1)
    # inline buttons
    
    item1 = types.InlineKeyboardButton(const.material_help_name, callback_data=const.material_help)
    item2 = types.InlineKeyboardButton(const.apos_name, callback_data=const.apos)
    item3 = types.InlineKeyboardButton(const.dispensary_name, callback_data=const.dispensary)
    item5 = types.InlineKeyboardButton(const.discounts_name, callback_data=const.discounts)
    item6 = types.InlineKeyboardButton(const.sos_name, callback_data=const.sos)
    items = [item1, item2, item3, item5, item6]
    for i in items:
        markup.row(i)
    if view == const.send:
        bot.send_message(message.chat.id, const.start_menu_txt, reply_markup=markup)
    elif view == const.edit:
        bot.edit_message_text(chat_id=message.chat.id, text=const.start_menu_txt, reply_markup=markup,
                              message_id=message.message_id)


def send_email(bot, message, email, users):
    if email[-13:] == const.phystech_email:  # checking if it's a phystech email
        if gs.find_user_in_profkom_list(email):  # checking if it is in labor union table
            bot.send_message(message.chat.id, const.sent_code_txt)
            # generating confirmation code
            temp = time.gmtime()
            code = rand(temp)
            # sending confirmation code to the user
            EmailSender.send_email(email, code)

            users[str(message.from_user.id)][const.auth_status] = const.code_wait
            users[str(message.from_user.id)][const.code] = code
            # updating users.json
            users_file_dump(users)
        else:
            bot.send_message(message.chat.id, const.not_in_union_txt)
            users[str(message.from_user.id)][const.auth_status] = const.not_auth
            # updating users.json
            users_file_dump(users)
    else:
        bot.send_message(message.chat.id, const.not_email_txt)


def check_code(bot, message, key, users):
    if key == str(users[str(message.from_user.id)][const.code]):
        # checking in the user texted the right confirmation code from the email
        bot.send_message(message.chat.id, const.email_authorized_txt)
        start_menu(bot, message, const.send)
        users[str(message.from_user.id)][const.auth_status] = const.auth
        # updating users.json
        users_file_dump(users)
    else:
        bot.send_message(message.chat.id, "Код " + key + " неверный ❌\nНапишите код из письма")
        users[str(message.from_user.id)][const.auth_status] = const.code_wait
        # updating users.json
        users_file_dump(users)


def discount_menu(bot, call):
    markup = types.InlineKeyboardMarkup(row_width=1)
    # inline buttons
    
    [companies, discrs, tutorials, enddates] = gs.load_bonuses()

    items = []
    for i in range(len(companies)):
        
        # bonus is out of date
        if date.fromisoformat(enddates[i]) <= date.today():
            continue

        item = types.InlineKeyboardButton(companies[i], callback_data=companies[i])
        items.append(item)

    for i in range(0, len(items) - 1, 2):
        markup.row(items[i], items[i + 1])

    bot.edit_message_text(chat_id=call.message.chat.id, text=const.discount_menu_txt,
                          message_id=call.message.message_id, reply_markup=markup)

    return [companies, discrs, tutorials, enddates] 


def back_button(data):
    markup = types.InlineKeyboardMarkup(row_width=1)
    back = types.InlineKeyboardButton(const.back_name, callback_data=data)
    markup.row(back)
    return markup


if __name__ == "__main__":
    print("You're running the wrong file!")
