# fish-shop

## Описание

fish-shop - это телегамм_бот-магазин. В данной демке продаем рыбу:)

[API Motlin](https://docs.moltin.com/api/)

## Пример работы

![Alt Text](http://ipic.su/img/img7/fs/fish-shop2.1561297725.gif)

## Требования

Для запуска скрипта требуется:

*Python 3.6*

## Как установить

1. Установить Python3:

(Windows):[python.org/downloads](https://www.python.org/downloads/windows/)

(Debian):

```sh
sudo apt-get install python3
sudo apt-get install python3-pip
```

2. Установить зависимости и скачать сам проект:

```sh
git clone https://github.com/Safintim/fish-shop.git
cd quiz-bot
pip3 install -r requirements.txt
```

3. Зарегистрироваться на [Redislabs](https://redislabs.com/) и получить адрес базы данных.

4. Персональные настройки:

Скрипт берет настройки из .env файла, где указаны токен телеграм-бота, токен чат-логгер-бота, хост, порт, пароль базы данных, а также токен, id и секретный ключ к moltin. Создайте файл .env вида:

```.env
ACCESS_TOKEN_MOLTIN=your_token
CLIENT_ID_MOLTIN=your_id
CLIENT_SECRET_MOLTIN=your_secret
TELEGRAM_BOT_TOKEN=your_token
LOGGER_BOT_TOKEN=your_token
LOGS_RECEIVER_ID=your_chat_id
REDIS_HOST=your_redis_host
REDIS_PASSWORD=your_redis_password
REDIS_PORT=your_redis_port
```

## Как использовать

```sh
python3 main.py
```

Часто слетает токен молтина. Получить токен можно с помощью функции *get_access_token*.
Либо просто запустить скрипт **api_moltin.py**, в консоль вывыдется токен.

```sh
python3 api_moltin.py
```

## Демо-боты

Данный бот готов к использованию. Пример работы указан на гифке выше.

* **_@deniskashoptest_bot_** - телеграм-бот-магазин
* **_@devmanlogging_bot_** - телеграм-логгер-бот, данный бот выполняет мониторинг телеграмм бота.
В случае ошибки придет уведомление о том, что "бот упал" и почему "бот упал",
 а также при запуске бот сообщит о запуске.

![Alt Text](http://ipic.su/img/img7/fs/quiz-log.1559419941.png)