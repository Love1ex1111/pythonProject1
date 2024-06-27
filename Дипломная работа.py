import telebot
from telebot import types
import random

TOKEN = '7123172947:AAEaVFi_tNexmNNBArIXZTEADZ_llfkLjKo'

bot = telebot.TeleBot(TOKEN)

# глобальное хранилище состояний пользователей
# (например, храним неизрасходованные попытки отгадать число)
USERS_STATES = dict()

# глобальное хранилище неправильного ввода числа
USERS_STATISTIC = dict()

# глобальное хранилище побед и поражений
USERS_RATING = dict()

# варианты ответов для 3 игры
dictionary = {
    1: "Думаю, да",
    2: "Думаю, нет",
    3: "Думаю, это возможно"
}

# баланс
USER_BALANCES = dict()

s4et4ik = 0


@bot.message_handler(commands=['start'])
def start(message):
    button_information = types.KeyboardButton('Информация о боте')
    button_guess_the_number = types.KeyboardButton('Игра угадай число от 1 до 10')
    button_casino_game = types.KeyboardButton('Игра казино')
    button_making_decisions = types.KeyboardButton('Бот ответит на любой вопрос '
                                                   '(Вопросы задавайте на которые нужно отвечать да/нет)')
    button_ball_game = types.KeyboardButton('Игра угадай под каким стаканчиком мячик')
    button_real_life = types.KeyboardButton('Игра с сюжэтом, похожая на реальную жизнь')
    button_balance = types.KeyboardButton('Посмотреть свой баланс')
    button_cliker = types.KeyboardButton('Кликер')

    markup = types.ReplyKeyboardMarkup(row_width=8, resize_keyboard=True)
    markup.add(button_information, button_cliker, button_guess_the_number, button_casino_game, button_making_decisions,
               button_ball_game, button_real_life, button_balance)

    bot.send_message(message.chat.id, 'Вас приветствует наш бот, выберите одну из функций бота пожалуйста',
                     reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'Информация о боте')
def information(message):
    bot.send_message(message.chat.id, 'Спасибо что воспользовали наш бот. Наш бот создан в основном для развлечений.'
                                      'Вы можете сыграть во множество игр. '
                                      'Так же у нас имеется баланс который вы можете пополнить.'
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
        s4et4ik += 1
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, 'Кнопка нажата '+str(s4et4ik)+str(' раз!'))
bot.polling(none_stop=True)

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
                USER_BALANCES[message.chat.id] = USER_BALANCES.get(message.chat.id, 0) + 60
                USERS_STATES.pop(message.chat.id)
            else:
                user['attempts'] -= 1
                if user['attempts'] > 0:
                    bot.send_message(message.chat.id, f'Неправильно((( Осталось попыток: {user["attempts"]}')
                else:
                    bot.send_message(message.chat.id,
                                     'Неправильно(( И попытки кончились(( Нажмите "Начать игру", чтобы отыграться')
                    USER_BALANCES[message.chat.id] = USER_BALANCES.get(message.chat.id, 0) - 30
                    USERS_STATES.pop(message.chat.id)
        except ValueError as e:
            if (USERS_STATISTIC[message.chat.id] % 3 == 0):
                bot.send_message(message.chat.id, 'eblan??????')
            bot.send_message(message.chat.id, 'Введите целое число от 1 до 10!!!')
        except Exception as e:
            print(e)
            bot.send_message(message.chat.id, 'Что-то пошло не так')


@bot.message_handler(func=lambda message: message.text == 'Игра казино')
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
                    USER_BALANCES[message.chat.id] = USER_BALANCES.get(message.chat.id, 0) + 20
                else:
                    bot.send_message(message.chat.id, "Вы проиграли!")
                    USER_BALANCES[message.chat.id] = USER_BALANCES.get(message.chat.id, 0) - 50
                    print(bot_number)
            elif user_guess == "2.":
                if bot_number in red_numbers:
                    bot.send_message(message.chat.id, "Вы победили!")
                    USER_BALANCES[message.chat.id] = USER_BALANCES.get(message.chat.id, 0) + 40
                else:
                    bot.send_message(message.chat.id, "Вы проиграли!")
                    USER_BALANCES[message.chat.id] = USER_BALANCES.get(message.chat.id, 0) -50
                    print(bot_number)
            elif user_guess == "3.":
                if bot_number in black_numbers:
                    bot.send_message(message.chat.id, "Вы победили!")
                    USER_BALANCES[message.chat.id] = USER_BALANCES.get(message.chat.id, 0) + 100
                else:
                    bot.send_message(message.chat.id, "Вы проиграли!")
                    USER_BALANCES[message.chat.id] = USER_BALANCES.get(message.chat.id, 0) - 130
                    print(bot_number)
            else:
                bot.send_message(message.chat.id, "Что-то пошло не так!")
        except Exception as e:
            bot.send_message(message.chat.id, "Что-то пошло не так!")


@bot.message_handler(func=lambda message: message.text == 'Бот ответит на любой вопрос '
                                                          '(Вопросы задавайте на которые нужно отвечать да/нет)')
def making_decisions(message):
    bot.send_message(message.chat.id, 'Введите вопрос пожалуйста')

    @bot.message_handler(content_types=['text'])
    def answer(message):
        random_key = random.choice(list(dictionary.keys()))
        random_value = dictionary[random_key]
        bot.send_message(message.chat.id, random_value)


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
            USER_BALANCES[message.chat.id] = USER_BALANCES.get(message.chat.id, 0) + 60
            return USER_BALANCES
        else:
            bot.send_message(message.chat.id, 'Ты проиграл, попробуй еще раз')
            USER_BALANCES[message.chat.id] = USER_BALANCES.get(message.chat.id, 0) - 35
            return USER_BALANCES

    @bot.message_handler(func=lambda message: message.text == 'стаканчик 2')
    def two(message):
        while ball == '2':
            bot.send_message(message.chat.id, 'Поздравляю с победой')
            USER_BALANCES[message.chat.id] = USER_BALANCES.get(message.chat.id, 0) + 60
            return USER_BALANCES
        else:
            bot.send_message(message.chat.id, 'Ты проиграл, попробуй еще раз')
            USER_BALANCES[message.chat.id] = USER_BALANCES.get(message.chat.id, 0) - 35
            return USER_BALANCES

    @bot.message_handler(func=lambda message: message.text == 'стаканчик 3')
    def two(message):
        while ball == '3':
            bot.send_message(message.chat.id, 'Поздравляю с победой')
            USER_BALANCES[message.chat.id] = USER_BALANCES.get(message.chat.id, 0) + 60
            return USER_BALANCES
        else:
            bot.send_message(message.chat.id, 'Ты проиграл, попробуй еще раз')
            USER_BALANCES[message.chat.id] = USER_BALANCES.get(message.chat.id, 0) - 35
            return USER_BALANCES

    @bot.message_handler(func=lambda message: message.text == 'Exit')
    def exit(message):
        start(message)


@bot.message_handler(func=lambda message: message.text == 'Игра с сюжэтом, похожая на реальную жизнь')
def real_life(message):
    bot.send_message(message.chat.id,
                     "Это игра с сюжетом. Каждый ваш последующий выбор будет влиять на вашу судьбу. "
                     "Не принимайте неверных решений. Удачи!")
    bot.send_message(message.chat.id, "Вы заблудились в лесу: ")
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    button_head_north = types.KeyboardButton("Идти на север")
    button_head_south = types.KeyboardButton("Идти на юг")
    markup.add(button_head_north, button_head_south)
    bot.send_message(message.chat.id, "Выберите направление:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'Идти на север')
def go_north(message):
    bot.send_message(message.chat.id, "Вы пошли на север, но шли так долго, что чуть не умерли от истощения.")
    button_st = types.KeyboardButton("Поплыть")
    button_g = types.KeyboardButton("Обойти")
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(button_st, button_g)
    bot.send_message(message.chat.id, "Вы пошли на север и вышли к болоту."
                                      " Обойдете или решите плыть?", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'Поплыть')
def stay(message):
    button_one = types.KeyboardButton("Пойти посмотреть")
    button_two = types.KeyboardButton("Пригнуться и спрятаться")
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(button_one, button_two)
    bot.send_message(message.chat.id, "Вы поплыли и остановились на центре болота,"
                                      " потому что что-то зашевелилось в кустах."
                                      "Вы пойдете посмотрите, или пригнетесь и спячитесь?", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'Пойти посмотреть')
def stay(message):
    bot.send_message(message.chat.id, "Там оказался медведь и он загрыз вас. Вы проиграли")
    USER_BALANCES[message.chat.id] = USER_BALANCES.get(message.chat.id, 0) - USER_BALANCES.get(message.chat.id, 0)
    USER_BALANCES[message.chat.id] = USER_BALANCES.get(message.chat.id, 0) + 100
    start(message)


@bot.message_handler(func=lambda message: message.text == 'Пригнуться и спрятаться')
def stay(message):
    bot.send_message(message.chat.id, "Медведь вылез из кустов и прошел мимо. Вы победили")
    USER_BALANCES[message.chat.id] = USER_BALANCES.get(message.chat.id, 0) * 6
    start(message)

@bot.message_handler(func=lambda message: message.text == 'Обойти')
def stay(message):
    button_one = types.KeyboardButton("Побежать оттуда")
    button_two = types.KeyboardButton("Пригнуться и спрятаться.")
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(button_one, button_two)
    bot.send_message(message.chat.id, "Вы вышли на лагерь разбойников", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'Побежать оттуда')
def stay(message):
    bot.send_message(message.chat.id, "Вы побежали и они вас заметили."
                                      "Вы долго бежали и вдруг почувствовали мягкость под ногами."
                                      "Жаль но это была ловушка разбойников. Вы проиграли.")
    USER_BALANCES[message.chat.id] = USER_BALANCES.get(message.chat.id, 0) - USER_BALANCES.get(message.chat.id, 0)
    USER_BALANCES[message.chat.id] = USER_BALANCES.get(message.chat.id, 0) + 100
    start(message)

@bot.message_handler(func=lambda message: message.text == 'Пригнуться и спрятаться.')
def stay(message):
    bot.send_message(message.chat.id, "Вы пригнулись. когда они заснули вы ограбили их и спокойно ушли оттуда."
                                      "Вы молодец, ведь вы победили и наткнулись на пасхалку."
                                      "Вам начисляется 1000 монет если отгадаете ответ на вопрос:")

    button_one = types.KeyboardButton("Сыграть супер игру и ответить на вопрос")
    button_two = types.KeyboardButton("Выйти в меню и просто забрать выйгрыш")
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(button_one, button_two)
    bot.send_message(message.chat.id, "Вы вышли на лагерь разбойников", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'Выйти в меню и просто забрать выйгрыш')
def stay(message):
    bot.send_message(message.chat.id, "Жаль что не захотели сыграть в супер игру, но вы победили. "
                                      "Поздравляю с победой")
    USER_BALANCES[message.chat.id] = USER_BALANCES.get(message.chat.id, 0) * 6
    start(message)


@bot.message_handler(func=lambda message: message.text == 'Сыграть супер игру и ответить на вопрос')
def stay(message):
    bot.send_message(message.chat.id, "А вы рискованный человек. Мне нравится ваш ход мыслей!!!")

    button_one = types.KeyboardButton("2016")
    button_two = types.KeyboardButton("1992")
    button_tree = types.KeyboardButton("1998")
    button_fore = types.KeyboardButton("2003")
    markup = types.ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)
    markup.add(button_one, button_two, button_tree, button_fore)
    bot.send_message(message.chat.id, "И так вопрос: В каком году в Белоруссии была денежная реформа,"
                                      "а именно были введены деньги,"
                                      " которыми мы пользуемся сейчас?",reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == '2016')
def stay(message):
    bot.send_message(message.chat.id, "ИИИИИИИ ВЫ ПОБЕДИЛИ В СУПЕР ИГРЕ!!!!!!!!! ВЫ ОГРОМНЫЙ МОЛОДЕЦ!!!!!")
    USER_BALANCES[message.chat.id] = USER_BALANCES.get(message.chat.id, 0) + 1000
    USER_BALANCES[message.chat.id] = USER_BALANCES.get(message.chat.id, 0) * 6
    start(message)

@bot.message_handler(func=lambda message: message.text == '1992')
def stay(message):
    bot.send_message(message.chat.id, "Увы, но вы проиграли, не расстраивайтесь у вас точно все получится.")
    USER_BALANCES[message.chat.id] = USER_BALANCES.get(message.chat.id, 0) - USER_BALANCES.get(message.chat.id, 0)
    USER_BALANCES[message.chat.id] = USER_BALANCES.get(message.chat.id, 0) + 100
    start(message)

@bot.message_handler(func=lambda message: message.text == '1998')
def stay(message):
    bot.send_message(message.chat.id, "Увы, но вы проиграли, не расстраивайтесь у вас точно все получится.")
    USER_BALANCES[message.chat.id] = USER_BALANCES.get(message.chat.id, 0) - USER_BALANCES.get(message.chat.id, 0)
    USER_BALANCES[message.chat.id] = USER_BALANCES.get(message.chat.id, 0) + 100
    start(message)


@bot.message_handler(func=lambda message: message.text == '2003')
def stay(message):
    bot.send_message(message.chat.id, "Увы, но вы проиграли, не расстраивайтесь у вас точно все получится.")
    USER_BALANCES[message.chat.id] = USER_BALANCES.get(message.chat.id, 0) - USER_BALANCES.get(message.chat.id, 0)
    USER_BALANCES[message.chat.id] = USER_BALANCES.get(message.chat.id, 0) + 100
    start(message)


@bot.message_handler(func=lambda message: message.text == 'Идти на юг')
def go_south(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    button_stay = types.KeyboardButton("Отдохнуть")
    button_go = types.KeyboardButton("Пойти дальше")
    markup.add(button_stay, button_go)
    bot.send_message(message.chat.id, "Вы пошли на юг и вышли к опушке."
                                      " Продолжать идти или остаться отдохнуть?", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'Отдохнуть')
def stay(message):
    bot.send_message(message.chat.id, "Вы остались на опушке и вас убил медведь. Вы проиграли")
    USER_BALANCES[message.chat.id] = USER_BALANCES.get(message.chat.id, 0) - USER_BALANCES.get(message.chat.id, 0)
    USER_BALANCES[message.chat.id] = USER_BALANCES.get(message.chat.id, 0) + 100
    start(message)


@bot.message_handler(func=lambda message: message.text == 'Пойти дальше')
def continue_going(message):
    bot.send_message(message.chat.id, "Вы пошли дальше и вышли на шоссе. Вы спасены! Победа!")
    USER_BALANCES[message.chat.id] = USER_BALANCES.get(message.chat.id, 0) * 6
    start(message)


@bot.message_handler(func=lambda message: message.text == 'Посмотреть свой баланс')
def balance(message):
    bot.send_message(message.chat.id, f'Ваш баланс составляет: {USER_BALANCES[message.chat.id]}')


bot.infinity_polling()