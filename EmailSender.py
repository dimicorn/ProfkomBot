import smtplib
import ssl
import json


def send_email(receiver, key):
    with open("config.json") as f:
        config = json.load(f)
    port = 587  # For starttls
    smtp_server = "smtp.mail.ru"
    sender_email = config["sender_email"]
    receiver_email = receiver
    password = config["sender_email_password"]
    # FixMe: make that the email was in russian and add email subject
    message = "Subject: Сonfirmation code\n" \
              "\n\nHello! Your code to confirm the mail of the trade union committee:\n" + str(key) + \
              "\nSincerely,\n profkomBot "  # 🤖

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)


if __name__ == "__main__":
    print("You're running the wrong file!")
