import time, threading, schedule
from telebot import TeleBot
from dataclasses import dataclass

from config import token


@dataclass
class Messages:
    hello = 'Привет! Я предупреждаю о рабочих встречах.'
    info = 'Введи /add, чтобы добавить рабочую встречу.'
    remainder = 'Ждем тебя на встрече в '


bot = TeleBot(token)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, Messages.hello)

@bot.message_handler(commands=['help'])
def send_info(message):
    bot.send_message(message.chat.id, Messages.info)

@bot.message_handler(commands=['add'])
def add_meeting(message):
    bot.send_message(message.chat.id, 'Введи время в формате: hh:mm')
    bot.register_next_step_handler(message, get_time)

def send_remainder(chat_id, data_time):
    bot.send_message(chat_id, Messages.remainder + data_time)

def get_time(message):
    date_time = message.text
    bot.send_message(message.chat.id, 'Добавлено: ' + date_time)
    schedule.every().wednesday.at(date_time).do(send_remainder, date_time)

def main() -> None:
    threading.Thread(target=bot.infinity_polling, name='bot_infinity_polling', daemon=True).start()

    while True:
        schedule.run_pending()
        time.sleep(1)

    # bot.polling(none_stop=True)


if __name__ == '__main__':
    main()
