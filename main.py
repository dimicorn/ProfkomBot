import telebot
from telebot import types
import json
import functions as funcs
import constants as const


class Storage:
    bonuses_data = []

def main():
    with open(const.files["config"]) as a:
        config = json.load(a)
    a.close()

    token = config["token"]
    bot = telebot.TeleBot(token)
    

    # defining /start command
    @bot.message_handler(commands=[const.start])
    def welcome(message):
        # loading all authorized users
        users = funcs.users_file_load()
        cur_id = str(message.from_user.id)

        if cur_id in users and users[cur_id][const.auth_status] == const.auth:
            # user is not first time using bot and is authorized
            funcs.start_menu(bot, message, const.send)

        else:  # user is not authorized/first time using the bot
            users[cur_id] = \
                {const.id: message.from_user.id, 
                 const.auth_status: const.not_auth, 
                 const.code: const.no_code}

            markup = types.InlineKeyboardMarkup(row_width=2)
            # inline buttons
            item1 = types.InlineKeyboardButton(const.yes_name, callback_data="in_union")
            item2 = types.InlineKeyboardButton(const.no_name, callback_data="not_in_union")
            markup.row(item1, item2)
            bot.send_message(message.chat.id, const.txts["hi"], reply_markup=markup)
            # updating users.json
            funcs.users_file_dump(users)

    # defining messages to the bot
    @bot.message_handler(content_types=[const.text])
    def echo(message):
        # loading users
        users = funcs.users_file_load()
        cur_id = str(message.from_user.id)

        if users[cur_id][const.auth_status] == const.auth_in_process:
            email = message.text
            funcs.send_email(bot, message, email, users)

        elif users[cur_id][const.auth_status] == const.code_wait:
            key = message.text
            funcs.check_code(bot, message, key, users)
        else:
            bot.send_message(message.chat.id, const.txts["sorry"])

    # buttons interaction
    @bot.callback_query_handler(func=lambda call: True)
    def callback_inline(call):
        # loading users
        users = funcs.users_file_load()

        try:
            if call.message:
                bot.answer_callback_query(call.id, show_alert=False, text=const.bot_emoji)
                
                if call.data == "in_union":
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                          text=const.txts["send_email"])
                    users[str(call.message.chat.id)][const.auth_status] = const.auth_in_process
                    # updating users.json
                    users_file = open(const.files["users"], "w")
                    json.dump(users, users_file)
                    users_file.close()
                elif call.data == "not_in_union":
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                          text=const.txts["union"], parse_mode=const.parse_mode)
                    # doc = open(const.prof_file, "rb")
                    # bot.send_document(call.message.chat.id, doc)
                if users[str(call.message.chat.id)][const.auth_status] == const.auth:
                    if call.data == "begin":
                        funcs.start_menu(bot, call.message, const.edit)
                    elif call.data == "material_help":
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                              text=const.txts["material_help"], parse_mode=const.parse_mode,
                                              reply_markup=funcs.back_button("begin"))
                    elif call.data == "apos":
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                              text=const.txts["apos"], parse_mode=const.parse_mode,
                                              reply_markup=funcs.back_button("begin"))
                        # doc = open(const.apos_file, "rb")
                        # bot.send_document(call.message.chat.id, doc)
                    elif call.data == "dispensary":
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                              text=const.txts["dispensary"], reply_markup=funcs.back_button("begin"))
                    elif call.data == "discounts":
                        Storage.bonuses_data = funcs.discount_menu(bot, call)
                    elif call.data == "sos":
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                              text=const.txts["sos"], reply_markup=funcs.back_button("begin"))
                    
                    #
                    # bonuses processing
                    # bonus_data = [companies, discrs, tutorials, enddates]
                    #
                    else:
                        for i in range(len(Storage.bonuses_data[0])):
                            if call.data == Storage.bonuses_data[0][i]:
                                bot.edit_message_text(chat_id=call.message.chat.id, 
                                                      message_id=call.message.message_id,
                                                      text=Storage.bonuses_data[1][i] + "\n\nСпособ получения: " + Storage.bonuses_data[2][i], 
                                                      reply_markup=funcs.back_button("discounts"))
        except Exception as e:
            print(repr(e))

    # run
    bot.polling(none_stop=True)


if __name__ == "__main__":
    main()
