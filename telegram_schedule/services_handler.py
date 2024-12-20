import os

from heroes.models import Hero
from users.models import User

from telegram_schedule.services_db import create_new_user_mentor, get_4_last_training_dates, get_teams, create_training, get_attendance

from config.settings import TG_API_TOKEN
import telebot


bot = telebot.TeleBot(TG_API_TOKEN)
actual_polls = []

# user_set_staff(1816252417)

"""

algorithm:

1) start_message handler
есть is_active: предложить действия
есть не активен: ждём активации
нет: ввод данных и регистрация (создать user, parent) offer_next_actions

2) text_messages handler
chose_action
CRUD?

NewHero ? C, Добавить новичка
Hero - CR, Посмотреть людей, Добавить новичка
Parent
Branch
Team
Training - CR, Отметить явку, Посмотреть явку
Course
Payment - CR, добавить (авто), посмотреть

### Payment example

Order #1621331113
1. Москва: 8000 (1 x 8000) Локация: Парк Лосиный остров, Абонемент: Абонемент на 4 тренировки 8000 руб.
The order is paid for.
Payment Amount: 8000 RUB
Payment ID: Tinkoff Payment: 5483772318

Purchaser information:
Родитель: Наталья Спивак
Дети: Федор Спивак
Phone: +79683664621

Additional information:
Transaction ID: 7694333:6959736881
Block ID: rec831865548
Form Name: Cart
https://xn--80aciihs1bdx6f.xn--p1ai/
-----

Order #1062728297
1. Москва: 2500 (1 x 2500) Локация: Одинцово, Абонемент: Пробная тренировка 2500 руб.
The order is paid for.
Payment Amount: 2500 RUB
Payment ID: Tinkoff Payment: 5452182606

Purchaser information:
Родитель: Андрей Волобуев
Дети: Иван Волобуев
Phone: +79164332541

Additional information:
Transaction ID: 7694333:6940307461
Block ID: rec831865548
Form Name: Cart
https://xn--80aciihs1bdx6f.xn--p1ai/
-----

###

3) poll answer handler
create_training

"""

@bot.message_handler(commands=['start'])
def start_message(message):

    # print(f'{message.from_user.username} (id {message.chat.id}) push START')

    try:
        response = User.objects.get(tg_id=message.from_user.id)
        bot.send_message(message.chat.id, f'Привет, {response.first_name}')
        if response.is_active:
            offer_next_actions(message)
        else:
            msg = bot.send_message(message.chat.id,
                                   f'Пользователь ещё не активирован',
                                   reply_markup=add_options_keyboard('start'))

    except Exception as e:

        text_message = f'''Привет {message.from_user.first_name}, я бот Heroes-CRM.
Для регистрации напиши свой телефон:'''

        msg = bot.send_message(message.chat.id, text_message)

        bot.register_next_step_handler(msg, input_phone_ask_email)


def input_phone_ask_email(message):

    phone = message.text

    try:
        us = User.objects.get(phone=phone)

        text_message = f'''Пользователь с таким телефоном уже есть в базе. Напиши другой телефон.'''
        msg = bot.send_message(message.chat.id, text_message)

        bot.register_next_step_handler(msg, input_phone_ask_email)

    except Exception as e:

        text_message = f'''Ещё напиши пожалуйста твой email:'''

        msg = bot.send_message(message.chat.id, text_message)

        bot.register_next_step_handler(msg, input_email_and_register, phone=phone)


def input_email_and_register(message, phone):

    email = message.text

    try:
        us = User.objects.get(email=email)

        text_message = f'''Пользователь с таким email уже есть в базе. Напиши другой email.'''
        msg = bot.send_message(message.chat.id, text_message)

        bot.register_next_step_handler(msg, input_email_and_register, phone=phone)

    except Exception as e:

        create_new_user_mentor(message, phone, email)

        text_message = f'''Приятно познакомиться, {message.from_user.first_name}! Внёс тебя в базу.
Администратор скоро одобрит заявку, и сможешь зайти на сайт.
Твой логин: {message.from_user.id}, пароль: 12345'''

        msg = bot.send_message(message.chat.id, text_message)

        offer_next_actions(message)


@bot.message_handler(func=lambda message: True)
def text_messages(message):
    # print(message.from_user.username, 'sent:', message.text)
    chose_action(message)


@bot.poll_answer_handler()
def handle_poll_answer(poll_answer):
    user_poll_input(poll_answer)


def start_polling():
    bot.infinity_polling(none_stop=True, interval=1)


##############


def offer_next_actions(message):

    msg = bot.send_message(message.chat.id,
                           "Выбери действие:",
                           reply_markup=add_options_keyboard())

    bot.register_next_step_handler(msg, chose_action)


def add_options_keyboard(next_key=None):

    if next_key is None:
        buttons = [
            # "Добавить маму или папу",
            # "Добавить героя",
            #       "Добавить новичка",
            #       "Добавить наставника или вожатую",
            #       "Добавить продукт",
            #       "Добавить платёж",
            #       "Добавить ячейку",
            "Отметить явку",
            "Посмотреть явку",
            "Посмотреть всех героев"
            ]

    elif next_key == "sex":
        buttons = ["м",
                       "ж"
                       ]
    elif next_key == "yn":
        buttons = ["Да",
                   "Нет"
                   ]
    elif next_key == "new" or next_key == "profile" or next_key == "feedback":
        buttons = ["True",
                       "False"
                       ]
    elif next_key == 'involvement':
        buttons = ['Школа мам',
                       'Институт',
                       'Вожатая',
                       'Гостевой',
                       'Выбыли',
                       'Наставник',
                       'Стажёр',
                       'Интересуется',
                       'Не интересуется',
                       'Сила дружбы'
                       ]
    elif next_key == 'mentor_level':
        buttons = ['Отважный'
                       'Искатель',
                       'Командир',
                       'Вожатая',
                       'Вожатая 0+'
                       ]
    elif next_key == 'start':
        buttons = ['/start'
                   ]
    elif next_key == 'date_':
        buttons = get_4_last_training_dates()
    elif next_key == 'team_':
        buttons = get_teams()
    else:
        buttons = None

    if buttons is not None:
        keyboard = get_reply_keyboard(buttons)
        return keyboard
    else:
        return None


def get_reply_keyboard(buttons: list):
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=len(buttons))

        b = []
        i = 0
        for text in buttons:
            button = telebot.types.KeyboardButton(text)
            b.append(button)

            i += 1
            if i > 1:
                keyboard.add(*b)
                b.clear()
                i = 0

        if i > 0:
            keyboard.add(*b)

        return keyboard


def get_inline_keyboard(buttons: dict):
        keyboard = telebot.types.InlineKeyboardMarkup(row_width=len(buttons))

        b = []
        i = 0
        for key, value in buttons.items():

            button = telebot.types.InlineKeyboardButton(value, callback_data=key)
            b.append(button)

            i += 1
            if i > 1:
                keyboard.add(*b)
                b.clear()
                i = 0

        if i > 0:
            keyboard.add(*b)

        return keyboard


def chose_action(message):

        # print('chose_action:', message.text)
        flag = True

        if message.text == 'Добавить наставника или вожатую':
            new_line = {
                'tg_id': '',
                'name': None,
                'surname': None,
                'phone': None,
                'mentor_level': ''
            }
            table_name = 'mentors'

        elif message.text == 'Добавить маму или папу':
            new_line = {
                'name': None,
                'surname': None,
                'phone': None,
                'involvement': None,
                'feedback': False,
                'sex': None
            }
            table_name = 'parents'

        elif message.text == 'Добавить героя':
            new_line = {
                'name': None,
                'surname': None,
                'birth_date': None,
                'sex': None,
                'mother_id': None,
                'father_id': None,
                'mentor_id': None,
                'cell_id': None,
                'new': None,
                'first_training_date': None,
                'planned_first_training_date': None,
                'profile': None,
                'photo': None
            }
            table_name = 'heroes'

        elif message.text == 'Добавить новичка':
            new_line = {
                'name': '',  # can skip
                'surname': '',
                'birth_date': '',
                'sex': '',
                'mother_id': None,  # mandatory
                'cell_id': None,
                'new': True,
                'planned_first_training_date': None,
            }
            table_name = 'heroes'

            '''
                    {'name': 'Имя', 'surname': '/skip',
                    'birth_date': '/skip', 'sex': True,
                    'mother_id': '2', 'cell_id': '2',
                    'new': True, 'planned_first_training_date': '11'}
                    hero added
            '''
        elif message.text == 'Добавить продукт':
            bot.send_message(message.chat.id, "Действие пока не реализовано")
            flag = False

        elif message.text == 'Добавить платёж':
            bot.send_message(message.chat.id, "Действие пока не реализовано")
            flag = False

        elif message.text == 'Добавить ячейку':
            bot.send_message(message.chat.id, "Действие пока не реализовано")
            flag = False

        elif message.text == 'Отметить явку':

            msg = bot.send_message(message.chat.id,
                                        f'Выберите дату:',
                                        reply_markup=add_options_keyboard("date_"))

            bot.register_next_step_handler(msg, chose_team)

            flag = False
            # bot.send_message(message.chat.id, "Действие пока не реализовано")

        elif message.text == 'Посмотреть явку':

            image_filename = get_attendance()
            text = 'Раз, два, три, ура!'

            with open(image_filename, 'rb') as img:

                msg = bot.send_photo(message.chat.id,
                                     photo=img,
                                     caption=text)

            os.remove(image_filename)

            flag = False

        elif message.text == 'Посмотреть всех людей':

            bot.send_message(message.chat.id, "Действие пока не реализовано")

            '''result = self.db.get_all_people()
            full_data = ["" + item[2] + ': ' +
                         (item[0] if item[0] is not None else "?") + ' ' +
                         (item[1] if item[1] is not None else "?")
                         for item in result]

            text_data = '\n'.join(full_data)

            self.bot.send_message(message.chat.id, text_data)
            flag = False'''

        else:
            bot.send_message(message.chat.id, "Действие не опознано")
            flag = False

        if flag:
            print('need to add smth')
            # user_text_input(message, new_line, None, self.db.insert_values, table_name, self.offer_next_actions)


################


def chose_team(message):

    msg = bot.send_message(message.chat.id,
                           f'Выберите отряд:',
                           reply_markup=add_options_keyboard("team_"))

    training_date = message.text
    bot.register_next_step_handler(msg, start_attendance_poll, training_date)


def start_attendance_poll(message, training_date):
    data = Hero.objects.all()

    team_name = message.text

    """options = [
        {'text': str(item), 'voter_count': 0} for item in data
    ]"""
    options = [str(item) for item in data]

    if not options:
        msg = bot.send_message(message.chat.id, 'There are no Heroes')

    elif len(options) == 1:
        msg = bot.send_message(message.chat.id,
                               f"Явка за {training_date}: {options[0]}",
                               reply_markup=add_options_keyboard("yn"))

        bot.register_next_step_handler(msg, set_attendance_of_one_hero, data[0], training_date, team_name)

    else:

        msg = bot.send_poll(message.chat.id,
                            f"Явка за {training_date}:",
                            options=options,
                            type='regular',
                            allows_multiple_answers=True,
                            is_anonymous=False,
                            reply_markup=add_options_keyboard()
                            )

        poll_structure = {'id': msg.poll.id,
                          'date': training_date,
                          'options': [item for item in data],
                          'team_name': team_name
                          }

        actual_polls.append(poll_structure)
        # print(actual_polls)

        bot.register_next_step_handler(msg, chose_action)


def user_poll_input(poll_answer):

    ids = [item['id'] for item in actual_polls]
    poll_id = ids.index(poll_answer.poll_id)
    poll = actual_polls[poll_id]

    heroes = []
    for index, hero in enumerate(poll['options']):
        if index in poll_answer.option_ids:
            heroes.append(hero)

    # print(f'answers: {poll_answer.option_ids}')
    # print(f'options: {poll['options']}')

    len_heroes = create_training(poll['team_name'],
                                 poll_answer.user.id,
                                 poll['date'],
                                 heroes)

    actual_polls.remove(poll)

    bot.send_message(poll_answer.user.id, f'{len_heroes} героев отмечены')


def set_attendance_of_one_hero(message, hero, date, team_name):

    if message.text == 'Да':

        create_training(team_name,
                        message.chat.id,
                        date,
                        [hero.id])

        msg = bot.send_message(message.chat.id,
                               f'1 герой отмечен',
                               reply_markup=add_options_keyboard())

    else:
        msg = bot.send_message(message.chat.id,
                               f'0 героев отмечены',
                               reply_markup=add_options_keyboard())

    bot.register_next_step_handler(msg, chose_action)
