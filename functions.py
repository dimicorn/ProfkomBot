import EmailSender
import GoogleSheets as gs
import time
import json
from telebot import types
import constants as const


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
    item4 = types.InlineKeyboardButton(const.train_name, callback_data=const.train)
    item5 = types.InlineKeyboardButton(const.discounts_name, callback_data=const.discounts)
    item6 = types.InlineKeyboardButton(const.sos_name, callback_data=const.sos)
    items = [item1, item2, item3, item4, item5, item6]
    for i in items:
        markup.row(i)
    if view == const.send:
        bot.send_message(message.chat.id, const.start_menu_txt, reply_markup=markup)
    elif view == const.edit:
        bot.edit_message_text(chat_id=message.chat.id, text=const.start_menu_txt, reply_markup=markup,
                              message_id=message.message_id)


def send_email(bot, message, email, users):
    if email[-13:] == const.phystech_email:  # checking if it's a phystech email
        if gs.find_user(email):  # checking if it is in labor union table
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
    item1 = types.InlineKeyboardButton(const.metro_name, callback_data=const.metro)
    item2 = types.InlineKeyboardButton(const.bonus_name, callback_data=const.bonus)
    item3 = types.InlineKeyboardButton(const.tele2_name, callback_data=const.tele2)
    item4 = types.InlineKeyboardButton(const.skyeng_name, callback_data=const.skyeng)
    item5 = types.InlineKeyboardButton(const.clock_name, callback_data=const.clock)
    item6 = types.InlineKeyboardButton(const.x_fit_name, callback_data=const.x_fit)
    item7 = types.InlineKeyboardButton(const.boltay_name, callback_data=const.boltay)
    item8 = types.InlineKeyboardButton(const.theory_name, callback_data=const.theory)
    item9 = types.InlineKeyboardButton(const.schnitzel_name, callback_data=const.schnitzel)
    item10 = types.InlineKeyboardButton(const.herb_store_name, callback_data=const.herb_store)
    item11 = types.InlineKeyboardButton(const.driving_school_name, callback_data=const.driving_school)
    item12 = types.InlineKeyboardButton(const.buffet_name, callback_data=const.buffet)
    item13 = types.InlineKeyboardButton(const.back_name, callback_data=const.begin)
    items = [item1, item2, item3, item4, item5, item6, item7, item8, item9, item10, item11, item12,
             item13]
    for i in range(0, len(items) - 1, 2):
        markup.row(items[i], items[i + 1])
    markup.row(item13)
    bot.edit_message_text(chat_id=call.message.chat.id, text=const.discount_menu_txt,
                          message_id=call.message.message_id, reply_markup=markup)


def back_button(data):
    markup = types.InlineKeyboardMarkup(row_width=1)
    back = types.InlineKeyboardButton(const.back_name, callback_data=data)
    markup.row(back)
    return markup


if __name__ == "__main__":
    print("You're running the wrong file!")
