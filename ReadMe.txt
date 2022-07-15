main.py --- файл для запуска телеграм бота,
функционал бота и авторизация пользователей написана в нем.

EmailSender.py --- модуль по отсылке кодов подтверждения на почту пользователей.

GoogleSheets.py --- поиск пользователя в гугл таблице профсоюза, выгрузка скидок профсоюза

users.json --- файл со статусом пользователей, кодами авторизации и id.

configs/config.json --- файл с токеном бота, почтой профкома и паролем от нее.

configs/bonus_config.json --- файл для конфигурации и взаимодействия с гугл таблицей бонусов
configs/profkomlist_config.json --- файл для конфигурации и взаимодействия с гугл таблицей членов профсоюза

Как установить python3 на сервере:
https://computingforgeeks.com/install-latest-python-on-centos-linux/

Для запуска на сервере:
В командной строке:
ssh -p 10018 user@proxy2.cod.phystech.edu
Пишешь пароль от user - "password"
cd profkom
cd ProfkomBot
screen
ping 64.0.0.0 -c 2 -w2 || wget -qO - "login.telecom.mipt.ru/bin/login.cgi?login=1217659&memorize=
on&password=((wget login.telecom.mipt.ru/bin/getqc.cgi -qO -; echo -n 262611) | md5sum - | head -c32 )"
python3.9 main.py
ctrl+A+D
ctrl+D
закрываешь терминал

Проверь, что закрыл лишние окна!
screen -ls --- показывает все открытые окна
Ex: 23520.pts-6.porkypig --- <id> = 23520
screen -r <id> --- переходишь в нужное окно
kill <id> --- закрываешь окно
