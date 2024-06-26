import telebot
from telebot import types
import random
import webbrowser

answers = ['Я не понял, что ты хочешь сказать.', 'Извини, я тебя не понимаю.', 'Я не знаю такой команды.',
           'Мой разработчик не говорил, что отвечать в такой ситуации... >_<']

USERS_STATES = dict()

USERS_STATISTIC = dict()

USERS_RATING = dict()

dictionary = {
    1: "Думаю, да",
    2: "Думаю, нет",
    3: "Думаю, это возможно"
}

bot = telebot.TeleBot('')

schetchik = dict()


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Want to Clik")
    button3 = types.KeyboardButton("🎰 Casino")
    button4 = types.KeyboardButton('📖 Write to the developer')
    markup.row(button1)
    markup.row(button3, button4)

    if message.text == '/start':
        bot.send_message(message.chat.id,
                         f'Hello, {message.from_user.first_name}!\nI am a clicker bot!\nКонтакт моего разработчика: https://t.me/Why_you_skared',
                         reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Перекинул тебя в главном меню! Выбирай!', reply_markup=markup)


@bot.message_handler()
def info(message):
    if message.text == "Want to Clik":
        clikChapter(message)
    elif message.text == "See balance":
        balanceChapter(message)
    elif message.text == "🎰 Casino":
        casinoChapter(message)
    elif message.text == "Money":
        def callback_hearts(call):
            if call.data == "Money":
                global schetchik
                schetchik += 10
                bot.send_message(call.message.chat.id, 'You have clicked ' + str(schetchik) + str(' times!'))
    elif message.text == "🔹Game guess the number from 1 to 10":
        @bot.message_handler(commands=['🔹Game guess the number from 1 to 10'])
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
                    schetchik[message.chat.id] = schetchik.get(message.chat.id, 0) + 60
                    USERS_STATES.pop(message.chat.id)
                else:
                    user['attempts'] -= 1
                    if user['attempts'] > 0:
                        bot.send_message(message.chat.id, f'Неправильно((( Осталось попыток: {user["attempts"]}')
                    else:
                        bot.send_message(message.chat.id,
                                         'Неправильно(( И попытки кончились(( Нажмите "Начать игру", чтобы отыграться')
                        schetchik[message.chat.id] = schetchik.get(message.chat.id, 0) - 30
                        USERS_STATES.pop(message.chat.id)
            except ValueError as e:
                if (USERS_STATISTIC[message.chat.id] % 3 == 0):
                    bot.send_message(message.chat.id, 'eblan??????')
                bot.send_message(message.chat.id, 'Введите целое число от 1 до 10!!!')
            except Exception as e:
                print(e)
                bot.send_message(message.chat.id, 'Что-то пошло не так')
    elif message.text == "🔹Casino game":
        def casino_game(message):
            bot.send_message(message.chat.id,
                             "Это игра казино. Здесь бот загадал число, а вы должны угадать цвет этого "
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
                        schetchik[message.chat.id] = schetchik.get(message.chat.id, 0) + 20
                    else:
                        bot.send_message(message.chat.id, "Вы проиграли!")
                        schetchik[message.chat.id] = schetchik.get(message.chat.id, 0) - 50
                        print(bot_number)
                elif user_guess == "2.":
                    if bot_number in red_numbers:
                        bot.send_message(message.chat.id, "Вы победили!")
                        schetchik[message.chat.id] = schetchik.get(message.chat.id, 0) + 40
                    else:
                        bot.send_message(message.chat.id, "Вы проиграли!")
                        schetchik[message.chat.id] = schetchik.get(message.chat.id, 0) - 50
                        print(bot_number)
                elif user_guess == "3.":
                    if bot_number in black_numbers:
                        bot.send_message(message.chat.id, "Вы победили!")
                        schetchik[message.chat.id] = schetchik.get(message.chat.id, 0) + 100
                    else:
                        bot.send_message(message.chat.id, "Вы проиграли!")
                        schetchik[message.chat.id] = schetchik.get(message.chat.id, 0) - 130
                        print(bot_number)
                else:
                    bot.send_message(message.chat.id, "Что-то пошло не так!")
            except Exception as e:
                bot.send_message(message.chat.id, "Что-то пошло не так!")
    elif message.text == "🔹The bot will answer any question. Ask questions that require yes/no answers)":
        def making_decisions(message):
            bot.send_message(message.chat.id, 'Введите вопрос пожалуйста')

        ball = random.randint(1, 3)
        @bot.message_handler(content_types=['text'])
        def answer(message):
            random_key = random.choice(list(dictionary.keys()))
            random_value = dictionary[random_key]
            bot.send_message(message.chat.id, random_value)
    elif message.text == "🔹Game guess which cup the ball is under":
        def ball_game(message):
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
                schetchik[message.chat.id] = schetchik.get(message.chat.id, 0) + 60
                return schetchik
            else:
                bot.send_message(message.chat.id, 'Ты проиграл, попробуй еще раз')
                schetchik[message.chat.id] = schetchik.get(message.chat.id, 0) - 35
                return schetchik

        @bot.message_handler(func=lambda message: message.text == 'стаканчик 2')
        def two(message):
            while ball == '2':
                bot.send_message(message.chat.id, 'Поздравляю с победой')
                schetchik[message.chat.id] = schetchik.get(message.chat.id, 0) + 60
                return schetchik
            else:
                bot.send_message(message.chat.id, 'Ты проиграл, попробуй еще раз')
                schetchik[message.chat.id] = schetchik.get(message.chat.id, 0) - 35
                return schetchik

        @bot.message_handler(func=lambda message: message.text == 'стаканчик 3')
        def two(message):
            while ball == '3':
                bot.send_message(message.chat.id, 'Поздравляю с победой')
                schetchik[message.chat.id] = schetchik.get(message.chat.id, 0) + 60
                return schetchik
            else:
                bot.send_message(message.chat.id, 'Ты проиграл, попробуй еще раз')
                schetchik[message.chat.id] = schetchik.get(message.chat.id, 0) - 35
                return schetchik

        @bot.message_handler(func=lambda message: message.text == 'Exit')
        def exit(message):
            start(message)
    elif message.text == "🔹A game with a plot similar to real life.":
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
            schetchik[message.chat.id] = schetchik.get(message.chat.id, 0) - schetchik.get(message.chat.id,
                                                                                           0)
            schetchik[message.chat.id] = schetchik.get(message.chat.id, 0) + 100
            start(message)

        @bot.message_handler(func=lambda message: message.text == 'Пригнуться и спрятаться')
        def stay(message):
            bot.send_message(message.chat.id, "Медведь вылез из кустов и прошел мимо. Вы победили")
            schetchik[message.chat.id] = schetchik.get(message.chat.id, 0) * 6
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
            schetchik[message.chat.id] = schetchik.get(message.chat.id, 0) - schetchik.get(message.chat.id,
                                                                                           0)
            schetchik[message.chat.id] = schetchik.get(message.chat.id, 0) + 100
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
            schetchik[message.chat.id] = schetchik.get(message.chat.id, 0) * 6
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
                                              " которыми мы пользуемся сейчас?", reply_markup=markup)

        @bot.message_handler(func=lambda message: message.text == '2016')
        def stay(message):
            bot.send_message(message.chat.id, "ИИИИИИИ ВЫ ПОБЕДИЛИ В СУПЕР ИГРЕ!!!!!!!!! ВЫ ОГРОМНЫЙ МОЛОДЕЦ!!!!!")
            schetchik[message.chat.id] = schetchik.get(message.chat.id, 0) + 1000
            schetchik[message.chat.id] = schetchik.get(message.chat.id, 0) * 6
            start(message)

        @bot.message_handler(func=lambda message: message.text == '1992')
        def stay(message):
            bot.send_message(message.chat.id, "Увы, но вы проиграли, не расстраивайтесь у вас точно все получится.")
            schetchik[message.chat.id] = schetchik.get(message.chat.id, 0) - schetchik.get(message.chat.id,
                                                                                           0)
            schetchik[message.chat.id] = schetchik.get(message.chat.id, 0) + 100
            start(message)

        @bot.message_handler(func=lambda message: message.text == '1998')
        def stay(message):
            bot.send_message(message.chat.id, "Увы, но вы проиграли, не расстраивайтесь у вас точно все получится.")
            schetchik[message.chat.id] = schetchik.get(message.chat.id, 0) - schetchik.get(message.chat.id,
                                                                                           0)
            schetchik[message.chat.id] = schetchik.get(message.chat.id, 0) + 100
            start(message)

        @bot.message_handler(func=lambda message: message.text == '2003')
        def stay(message):
            bot.send_message(message.chat.id, "Увы, но вы проиграли, не расстраивайтесь у вас точно все получится.")
            schetchik[message.chat.id] = schetchik.get(message.chat.id, 0) - schetchik.get(message.chat.id,
                                                                                           0)
            schetchik[message.chat.id] = schetchik.get(message.chat.id, 0) + 100
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
            schetchik[message.chat.id] = schetchik.get(message.chat.id, 0) - schetchik.get(message.chat.id,
                                                                                           0)
            schetchik[message.chat.id] = schetchik.get(message.chat.id, 0) + 100
            start(message)

        @bot.message_handler(func=lambda message: message.text == 'Пойти дальше')
        def continue_going(message):
            bot.send_message(message.chat.id, "Вы пошли дальше и вышли на шоссе. Вы спасены! Победа!")
            schetchik[message.chat.id] = schetchik.get(message.chat.id, 0) * 6
            start(message)
    elif message.text == '📖 Write to the developer':
        webbrowser.open('https://t.me/Why_you_skared')
    elif message.text == '↩️ back':
        clikChapter(message)
    elif message.text == '↩️ back to menu':
        start(message)
    else:
        bot.send_message(message.chat.id, answers[random.randint(0, 3)])


def clikChapter(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Money")
    button2 = types.KeyboardButton('↩️ back')
    markup.row(button1)
    markup.row(button2)
    bot.send_message(message.chat.id, 'Welcome to the clicker game. 1 click = 1 coin.', reply_markup=markup)
    bot.send_message(message.chat.id, 'Click the button:', reply_markup=markup)


def balanceChapter(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("👛 See balance")
    button2 = types.KeyboardButton('↩️ Назад в меню')
    markup.row(button1, button2)
    bot.send_message(message.chat.id, 'Balance section.\nChoose one of the options:', reply_markup=markup)


def casinoChapter(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("🔹Game guess the number from 1 to 10")
    button2 = types.KeyboardButton("🔹Casino game")
    button3 = types.KeyboardButton("🔹The bot will answer any question. Ask questions that require yes/no answers)")
    button4 = types.KeyboardButton("🔹Game guess which cup the ball is under")
    button5 = types.KeyboardButton("🔹A game with a plot similar to real life.")
    button6 = types.KeyboardButton('↩️ back to menu')
    markup.row(button1, button2)
    markup.row(button3, button4)
    markup.row(button5, button6)

    bot.send_message(message.chat.id, 'A list of casino options is available to you:', reply_markup=markup)


bot.polling(none_stop=True)
