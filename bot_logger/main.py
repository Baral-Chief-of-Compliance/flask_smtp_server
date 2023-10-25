import telebot
from dotenv import load_dotenv
import os
from db_bot_tools import add_admin, get_status_logger, turn_off_logger, turn_on_logger



load_dotenv()



bot = telebot.TeleBot(os.getenv("LOGGER_TELEGRAM_BOT_API_KEY"))

markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
btn1 = telebot.types.KeyboardButton('Статус логирования')
btn2 = telebot.types.KeyboardButton('Отключить логирование')
btn3 = telebot.types.KeyboardButton('Включить логирование')
markup.add(btn1, btn2, btn3)


@bot.message_handler(commands = ['start'])
def start(message):
    user_id = message.from_user.id

    add_admin(str(user_id))

    bot.send_message(message.from_user.id, f"Добро пожаловать!\n Это логер бот рассылки. \n Логирование включено", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == 'Статус логирования':

        status_log = get_status_logger(message.from_user.id)

        if status_log == 'on':
            bot.send_message(message.from_user.id, f"Статус: включено", reply_markup=markup)
        elif status_log == 'off':
            bot.send_message(message.from_user.id, f"Статус: выключено", reply_markup=markup)

    elif message.text == 'Отключить логирование':

        turn_off_logger(message.from_user.id)

        bot.send_message(message.from_user.id, f"Логирование выключено", reply_markup=markup)

    elif message.text == 'Включить логирование':

        turn_on_logger(message.from_user.id)

        bot.send_message(message.from_user.id, f"Логирование включено", reply_markup=markup)

    else:
        bot.send_message(message.from_user.id, f"такой команды я не понимаю", reply_markup=markup)

print("ss")


bot.polling(none_stop=True, interval=0)