import telebot
from telebot import types
bot = telebot.TeleBot('7123172947:AAEaVFi_tNexmNNBArIXZTEADZ_llfkLjKo')
s4et4ik = 0
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Want to Clik")
    btn2 = types.KeyboardButton("See balance")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id,"Hello, I'm a clicker bot ", reply_markup=markup)
@bot.message_handler(func=lambda message: message.text == 'Want to Clik')
def hearts(message):
    keyboard_two = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    callback = types.InlineKeyboardButton(text="Money", callback_data="knopka")
    end = types.KeyboardButton("End")
    keyboard_two.add(end)
    keyboard.add(callback)
    bot.send_message(chat_id=message.chat.id, text="Добро пожаловать в игру кликер. 1 клик = 1 доллару",
                     reply_markup=keyboard_two)
    bot.send_message(chat_id=message.chat.id, text="Нажмите кнопку:", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_hearts(call):
    if call.data == 'knopka':
        global s4et4ik
        s4et4ik += 1
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, 'Кнопка нажата '+str(s4et4ik)+str(' раз!'))
bot.polling(none_stop=True)