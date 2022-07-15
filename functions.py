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
    with open(const.files["users"]) as f:
        users = json.load(f)
    f.close()
    return users


def users_file_dump(users):
    users_file = open(const.files["users"], "w")
    json.dump(users, users_file)
    users_file.close()


def start_menu(bot, message, view):
    markup = types.InlineKeyboardMarkup(row_width=1)
    # inline buttons
    
    item1 = types.InlineKeyboardButton(const.material_help_name, callback_data="material_help")
    item2 = types.InlineKeyboardButton(const.apos_name, callback_data="apos")
    item3 = types.InlineKeyboardButton(const.dispensary_name, callback_data="dispensary")
    item5 = types.InlineKeyboardButton(const.discounts_name, callback_data="discounts")
    item6 = types.InlineKeyboardButton(const.sos_name, callback_data="sos")
    items = [item1, item2, item3, item5, item6]
    for i in items:
        markup.row(i)
    if view == const.send:
        bot.send_message(message.chat.id, const.txts["start_menu"], reply_markup=markup)
    elif view == const.edit:
        bot.edit_message_text(chat_id=message.chat.id, text=const.txts["start_menu"], reply_markup=markup,
                              message_id=message.message_id)


def send_email(bot, message, email, users):
    if email[-13:] == const.phystech_email:  # checking if it's a phystech email
        if gs.find_user_in_profkom_list(email):  # checking if it is in labor union table
            bot.send_message(message.chat.id, const.txts["sent_code"])
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
            bot.send_message(message.chat.id, const.txts["not_in_union"])
            users[str(message.from_user.id)][const.auth_status] = const.not_auth
            # updating users.json
            users_file_dump(users)
    else:
        bot.send_message(message.chat.id, const.txts["not_email"])


def check_code(bot, message, key, users):
    if key == str(users[str(message.from_user.id)][const.code]):
        # checking in the user texted the right confirmation code from the email
        bot.send_message(message.chat.id, const.txts["email_authorized"])
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
    
    back = types.InlineKeyboardButton(const.back_name, callback_data="begin")
    markup.row(back)

    bot.edit_message_text(chat_id=call.message.chat.id, text=const.txts["discount_menu"],
                          message_id=call.message.message_id, reply_markup=markup)

    return [companies, discrs, tutorials, enddates] 


def back_button(data):
    markup = types.InlineKeyboardMarkup(row_width=1)
    back = types.InlineKeyboardButton(const.back_name, callback_data=data)
    markup.row(back)
    return markup


if __name__ == "__main__":
    print("You're running the wrong file!")
