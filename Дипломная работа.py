import telebot
from telebot import types
import random
import webbrowser


TOKEN = '7123172947:AAEaVFi_tNexmNNBArIXZTEADZ_llfkLjKo'

bot = telebot.TeleBot(TOKEN)

# глобальное хранилище состояний пользователей
# (например, храним неизрасходованные попытки отгадать число)
USERS_STATES = dict()

# глобальное хранилище неправильного ввода числа
USERS_STATISTIC = dict()

# глобальное хранилище побед и поражений
USERS_RATING = dict()

# баланс
s4et4ik = 0
USER_BALANCES = dict()

@bot.message_handler(commands=['start'])
def start(message):
    button_information = types.KeyboardButton('Информация о боте')
    button_guess_the_number = types.KeyboardButton('Игра угадай число от 1 до 10')
    button_casino_game = types.KeyboardButton('🎰Игра казино🎰')
    button_ball_game = types.KeyboardButton('Игра угадай под каким стаканчиком мячик')
    button_balance = types.KeyboardButton('👛Посмотреть свой баланс👛')
    button_cliker = types.KeyboardButton('Кликер')
    button_write_to_the_developer = types.KeyboardButton('📖Написать разработчику📖')

    markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    markup.add(button_information, button_cliker, button_guess_the_number, button_casino_game,
               button_ball_game, button_balance, button_write_to_the_developer)

    bot.send_message(message.chat.id,
                     f'Hello, {message.from_user.first_name}!\nI am a clicker bot!\nКонтакт моего разработчика: https://t.me/Why_you_skared',
                     reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'Информация о боте')
def information(message):
    bot.send_message(message.chat.id, 'Спасибо что воспользовали наш бот. Наш бот создан в основном для развлечений.'
                                      'Вы можете сыграть во множество игр. '
                                      'Так же у нас имеется баланс который вы можете пополнить кликая на кнопку.'
                                      'Желаю вам удачной игры.')


@bot.message_handler(func=lambda message: message.text == 'Кликер')
def start_hearts(message):
    keyboard = types.InlineKeyboardMarkup()
    callback = types.InlineKeyboardButton(text="Money", callback_data="knopka")
    keyboard.add(callback)
    bot.send_message(chat_id=message.chat.id, text="Нажмите кнопку:", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_hearts(call):
    if call.data == 'knopka':
        global s4et4ik
        s4et4ik += 10
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, 'Кнопка нажата ')



@bot.message_handler(func=lambda message: message.text == 'Игра угадай число от 1 до 10')
def guess_the_number(message):
    number = random.randint(1, 10)
    USERS_STATES[message.chat.id] = {'number': number, 'attempts': 5}
    print(f'{USERS_STATES=}')
    bot.send_message(message.chat.id, 'Угадай число от 1 до 10, вы можете попробовать 5 раз.')

    @bot.message_handler(func=lambda message: message.chat.id in USERS_STATES)
    def put_the_number(message):
        user = USERS_STATES[message.chat.id]

        try:
            guess = int(message.text)

            if guess == user['number']:
                bot.send_message(message.chat.id,
                                 'Поздравляем, вы угадали число! '
                                 'Нажмите "Начать игру", чтобы сыграть ещё раз')
                USER_BALANCES[message.chat.id] = USER_BALANCES.get(message.chat.id, 0) + s4et4ik
                USER_BALANCES[message.chat.id] = USER_BALANCES.get(message.chat.id, 0) + 60
                USERS_STATES.pop(message.chat.id)
            else:
                user['attempts'] -= 1
                if user['attempts'] > 0:
                    bot.send_message(message.chat.id, f'Неправильно((( Осталось попыток: {user["attempts"]}')
                else:
                    bot.send_message(message.chat.id,
                                     'Неправильно(( И попытки кончились(( Нажмите "Начать игру", чтобы отыграться')
                    USER_BALANCES[message.chat.id] = USER_BALANCES.get(message.chat.id, 0) + s4et4ik
                    USER_BALANCES[message.chat.id] = USER_BALANCES.get(message.chat.id, 0) - 30
                    USERS_STATES.pop(message.chat.id)
        except ValueError as e:
            if (USERS_STATISTIC[message.chat.id] % 3 == 0):
                bot.send_message(message.chat.id, 'eblan??????')
            bot.send_message(message.chat.id, 'Введите целое число от 1 до 10!!!')
        except Exception as e:
            print(e)
            bot.send_message(message.chat.id, 'Что-то пошло не так')


@bot.message_handler(func=lambda message: message.text == '🎰Игра казино🎰')
def casino_game(message):
    bot.send_message(message.chat.id, "Это игра казино. Здесь бот загадал число, а вы должны угадать цвет этого "
                                      "числа. Числа от 1 до 100 включительно. Цвета: красный, белый, черный."
                                      " Если вы угадываете, вам на счет начисялются деньги. Если не угадали, деньги"
                                      " со счета снимают. Удачи!")
    bot.send_message(message.chat.id, "Бот загадал число. "
                                      "Введите пожалуйста на какой цвет ставите: если на белый напишите: 1. , "
                                      "если на красный напишите: 2. , "
                                      "если на черный: 3. "
                                      "(Обязательно напишите цифру потом точку, иначе не сработает.)")

    @bot.message_handler(content_types=["text"])
    def get_message(message):
        list_nums = list(range(1, 101))
        random.shuffle(list_nums)
        try:
            user_guess = str(message.text)
            bot_number = random.randint(1, 100)
            white_numbers = list_nums[2::3]
            red_numbers = list_nums[1:74:3]
            black_numbers = list_nums[76::3]
            if user_guess == "1.":
                if bot_number in white_numbers:
                    bot.send_message(message.chat.id, "Вы победили!")
                    USER_BALANCES[message.chat.id] = USER_BALANCES.get(message.chat.id, 0) + s4et4ik
                    USER_BALANCES[message.chat.id] = USER_BALANCES.get(message.chat.id, 0) + 20
                else:
                    bot.send_message(message.chat.id, "Вы проиграли!")
                    USER_BALANCES[message.chat.id] = USER_BALANCES.get(message.chat.id, 0) + s4et4ik
                    USER_BALANCES[message.chat.id] = USER_BALANCES.get(message.chat.id, 0) - 50
                    print(bot_number)
            elif user_guess == "2.":
                if bot_number in red_numbers:
                    bot.send_message(message.chat.id, "Вы победили!")
                    USER_BALANCES[message.chat.id] = USER_BALANCES.get(message.chat.id, 0) + s4et4ik
                    USER_BALANCES[message.chat.id] = USER_BALANCES.get(message.chat.id, 0) + 40
                else:
                    bot.send_message(message.chat.id, "Вы проиграли!")
                    USER_BALANCES[message.chat.id] = USER_BALANCES.get(message.chat.id, 0) + s4et4ik
                    USER_BALANCES[message.chat.id] = USER_BALANCES.get(message.chat.id, 0) -50
                    print(bot_number)
            elif user_guess == "3.":
                if bot_number in black_numbers:
                    bot.send_message(message.chat.id, "Вы победили!")
                    USER_BALANCES[message.chat.id] = USER_BALANCES.get(message.chat.id, 0) + s4et4ik
                    USER_BALANCES[message.chat.id] = USER_BALANCES.get(message.chat.id, 0) + 100
                else:
                    bot.send_message(message.chat.id, "Вы проиграли!")
                    USER_BALANCES[message.chat.id] = USER_BALANCES.get(message.chat.id, 0) + s4et4ik
                    USER_BALANCES[message.chat.id] = USER_BALANCES.get(message.chat.id, 0) - 130
                    print(bot_number)
            else:
                bot.send_message(message.chat.id, "Что-то пошло не так!")
        except Exception as e:
            bot.send_message(message.chat.id, "Что-то пошло не так!")


@bot.message_handler(func=lambda message: message.text == 'Игра угадай под каким стаканчиком мячик')
def ball_game(message):
    ball = random.randint(1, 3)
    button_one = types.KeyboardButton('стаканчик 1')
    button_two = types.KeyboardButton('стаканчик 2')
    button_three = types.KeyboardButton('стаканчик 3')
    button_fore = types.KeyboardButton('Exit')
    markup = types.ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)
    markup.add(button_one, button_two, button_three, button_fore)
    bot.send_message(message.chat.id, 'Введите номер стаканчика под которым на ваше мнение лежит шарик: ',
                     reply_markup=markup)

    @bot.message_handler(func=lambda message: message.text == 'стаканчик 1')
    def first(message):
        while ball == '1':
            bot.send_message(message.chat.id, 'Поздравляю с победой')
            USER_BALANCES[message.chat.id] = USER_BALANCES.get(message.chat.id, 0) + s4et4ik
            USER_BALANCES[message.chat.id] = USER_BALANCES.get(message.chat.id, 0) + 60
            return USER_BALANCES
        else:
            bot.send_message(message.chat.id, 'Ты проиграл, попробуй еще раз')
            USER_BALANCES[message.chat.id] = USER_BALANCES.get(message.chat.id, 0) + s4et4ik
            USER_BALANCES[message.chat.id] = USER_BALANCES.get(message.chat.id, 0) - 35
            return USER_BALANCES

    @bot.message_handler(func=lambda message: message.text == 'стаканчик 2')
    def two(message):
        while ball == '2':
            bot.send_message(message.chat.id, 'Поздравляю с победой')
            USER_BALANCES[message.chat.id] = USER_BALANCES.get(message.chat.id, 0) + s4et4ik
            USER_BALANCES[message.chat.id] = USER_BALANCES.get(message.chat.id, 0) + 60
            return USER_BALANCES
        else:
            bot.send_message(message.chat.id, 'Ты проиграл, попробуй еще раз')
            USER_BALANCES[message.chat.id] = USER_BALANCES.get(message.chat.id, 0) + s4et4ik
            USER_BALANCES[message.chat.id] = USER_BALANCES.get(message.chat.id, 0) - 35
            return USER_BALANCES

    @bot.message_handler(func=lambda message: message.text == 'стаканчик 3')
    def two(message):
        while ball == '3':
            bot.send_message(message.chat.id, 'Поздравляю с победой')
            USER_BALANCES[message.chat.id] = USER_BALANCES.get(message.chat.id, 0) + s4et4ik
            USER_BALANCES[message.chat.id] = USER_BALANCES.get(message.chat.id, 0) + 60
            return USER_BALANCES
        else:
            bot.send_message(message.chat.id, 'Ты проиграл, попробуй еще раз')
            USER_BALANCES[message.chat.id] = USER_BALANCES.get(message.chat.id, 0) + s4et4ik
            USER_BALANCES[message.chat.id] = USER_BALANCES.get(message.chat.id, 0) - 35
            return USER_BALANCES

    @bot.message_handler(func=lambda message: message.text == 'Exit')
    def exit(message):
        start(message)

@bot.message_handler(func=lambda message: message.text == '👛Посмотреть свой баланс👛')
def balance(message):
    bot.send_message(message.chat.id, f'Ваш баланс составляет: {USER_BALANCES.get(message.chat.id, 0) + s4et4ik}')

@bot.message_handler(func=lambda message: message.text == '📖Написать разработчику📖')
def write_to_the_developer(message):
    webbrowser.open('https://t.me/Why_you_skared')


bot.infinity_polling()