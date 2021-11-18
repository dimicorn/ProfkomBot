import smtplib
from email.mime.text import MIMEText
from email.header import Header
import random
import config
import database

def check_email(message):
    email = message.text
    length = len(email)
    if email[length-13:length] == '@phystech.edu':
        send_code(message)
        text = 'На вашу почту выслан код, введите его'
        return text
    else:
        text = 'Вы указали неверную почту'
        return text


def send_code(message):

    code = random.randint(100000, 999999)
    print(code)

    # User Details
    receiver = message.text
    # Settings
    mail_sender = f'{config.login}'
    mail_receiver = f'{receiver}'
    username = f'{config.login}'
    password = f'{config.password}'
    server = smtplib.SMTP('smtp.gmail.com:587')

    # Content of mail
    subject = 'Верификация в Telegram Bot'
    body = f'Ваш код: {code} \n\nВведите его в чат'
    msg = MIMEText(body, 'plain', 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')

    # Sending mail
    server.starttls()
    server.ehlo()
    server.login(username, password)
    server.sendmail(mail_sender, mail_receiver, msg.as_string())
    server.quit()

    # Adding code to database
    database.add_code(message, code, receiver)


def check_code(message, user_code):
    db_code = database.check_code(message)
    if db_code == user_code:
        database.add_user(message)
        return 'Вы прошли верификацию'
    else:
        return 'Вы ввели неправильный код :(\n\nПопробуйте еще раз!'

