import time
import threading
import telebot
from telebot import types

bot = telebot.TeleBot('5755494991:AAHxV2VJs_bJeys2pwuFfFEiu56qFuk0fTc')

users = {}
@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    keyboard = types.InlineKeyboardMarkup()
    start_button = types.InlineKeyboardButton(text='Начать', callback_data='LetsGo')
    keyboard.add(start_button)
    bot.send_message(message.chat.id, f'''Привет, {str(message.chat.first_name)}! 
                                          Нажми Начать''', reply_markup=keyboard)
@bot.callback_query_handler(func=lambda  call: True)
def callback_worker(call):
    if call.data == 'LetsGo':
        bot.send_message(call.message.chat.id, 'Что будем запоминать?')

@bot.message_handler(content_types=['text'])
def get_message(message):
    alert = message.text
    chat_id = message.chat.id
    answer = f'{str(message.chat.first_name)}. Через сколько минут напомнить?'
    bot.send_message(message.chat.id, text=answer)
    bot.register_next_step_handler(message, get_time)
    users[chat_id] = [alert]

def get_time(message):

    timelaps = message.text
    chat_id = message.chat.id
    users[chat_id].insert(1, timelaps)
    while timelaps.isdigit() != True:
        bot.send_message(message.chat.id, 'Цифрами, пожалуйста 😉')
        bot.register_next_step_handler(message, get_time)
        users[chat_id].pop()
        break
    else:
        t = int(timelaps)*60
        time.sleep(t)
        check_in(message)

def check_in(message):
    chat_id = message.chat.id
    timelaps = users[chat_id][1]
    alert = users[chat_id][0]
    bot.send_message(message.chat.id, text=f'НАПОМИНАЮ: {alert}')

bot.polling(none_stop=True, timeout=20)