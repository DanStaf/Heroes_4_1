import os
import psycopg2

from heroes.models import Hero, Training, Cell, Parent
from users.models import User

from telegram_schedule.services_connector import create_new_user_mentor, get_4_last_training_dates, get_cells, \
    create_image, user_set_staff

from config.settings import TG_API_TOKEN, DATABASES
import telebot

bot = telebot.TeleBot(TG_API_TOKEN)
actual_polls = []

# user_set_staff(1816252417)


@bot.message_handler(commands=['start'])
def start_message(message):

    # print(f'{message.from_user.username} (id {message.chat.id}) push START')

    try:
        response = User.objects.get(tg_id=message.from_user.id)
        msg = bot.send_message(message.chat.id, f'Привет, {response.first_name}')
        offer_next_actions(message)

    except Exception as e:

        text_message = f'''Привет {message.from_user.first_name}, я бот Heroes-CRM.
Для регистрации напиши свой email.'''

        msg = bot.send_message(message.chat.id, text_message)

        bot.register_next_step_handler(msg, input_email_and_register)


def input_email_and_register(message):

    try:
        us = User.objects.get(email=message.text)

        text_message = f'''Пользователь с таким email уже есть в базе. Напиши другой email.'''
        msg = bot.send_message(message.chat.id, text_message)

        bot.register_next_step_handler(msg, input_email_and_register)

    except Exception as e:

        create_new_user_mentor(message)

        text_message = f'''Приятно познакомиться, {message.from_user.first_name}! Внёс тебя в базу.
Администратор скоро одобрит заявку, и сможешь зайти на сайт.'''

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
    elif next_key == 'date_':
        buttons = get_4_last_training_dates()
    elif next_key == 'cell_':
        buttons = get_cells()
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

            bot.register_next_step_handler(msg, chose_cell)

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


def chose_cell(message):

    msg = bot.send_message(message.chat.id,
                           f'Выберите ячейку:',
                           reply_markup=add_options_keyboard("cell_"))

    training_date = message.text
    bot.register_next_step_handler(msg, start_attendance_poll, training_date)


def start_attendance_poll(message, training_date):
    data = Hero.objects.all()

    cell_name = message.text

    """options = [
        {'text': str(item), 'voter_count': 0} for item in data
    ]"""
    options = [str(item) for item in data]
    # print(options)

    msg = bot.send_poll(message.chat.id,
                        f"Явка за {training_date}:",
                        options=options,
                        type='regular',
                        allows_multiple_answers=True,
                        is_anonymous=False,
                        reply_markup=add_options_keyboard()
                        )
    bot.register_next_step_handler(msg, chose_action)

    poll_structure = {'id': msg.poll.id,
                      'date': training_date,
                      'options': [item for item in data],
                      'cell_name': cell_name
                      }

    actual_polls.append(poll_structure)
    # print(actual_polls)


def user_poll_input(poll_answer):

    ids = [item['id'] for item in actual_polls]
    poll_id = ids.index(poll_answer.poll_id)
    poll = actual_polls[poll_id]

    user = User.objects.get(tg_id=poll_answer.user.id)
    mentor = Parent.objects.get(phone=user.phone)
    cell = Cell.objects.get(location=poll['cell_name'][:-9], day_time=poll['cell_name'][-8:])

    # print(f'answers: {poll_answer.option_ids}')
    # print(f'options: {poll['options']}')

    heroes = []
    for index, hero in enumerate(poll['options']):
        if index in poll_answer.option_ids:
            heroes.append(hero)

    tr = Training.objects.create(mentor=mentor,
                                 date=get_date_format(poll['date']),
                                 cell=cell
                                 )
    tr.heroes.add(*heroes)
    tr.save()

    actual_polls.remove(poll)

    bot.send_message(poll_answer.user.id, f'{len(heroes)} героев отмечены')


def get_date_format(text_date):

    # 'Значение “08.09.2024” должно быть в формате YYYY-MM-DD.'
    day = text_date[:2]
    mon = text_date[3:5]
    year = text_date[-4:]
    return year + '-' + mon + '-' + day


def get_attendance():
    """ use direct SQL request """

    dates = get_4_last_training_dates("%Y-%m-%d")
    dates_repr = get_4_last_training_dates("%b%d")

    conn_params = {
        "host": DATABASES['default']['HOST'],
        "database": DATABASES['default']['NAME'],
        "user": DATABASES['default']['USER'],
        "password": DATABASES['default']['PASSWORD']
    }

    cells = Cell.objects.all()

    total_result = []

    for cell in cells:

        query = """
                        SELECT
                        heroes_hero.id,
                        heroes_hero.name,
                        heroes_hero.surname"""

        for index, one_date_repr in enumerate(dates_repr):
            query += f""",
                        S{index}.training_date as {one_date_repr}"""

        query += """
                        from heroes_hero
                        """

        for index, one_date in enumerate(dates):
            query += f"""
                        FULL JOIN (SELECT
                          hero_id,
                          training_id,
                          true as training_date
                        FROM heroes_training_heroes A
                        INNER JOIN heroes_training T on A.training_id = T.id
                        WHERE T.date = '{one_date}' and T.cell_id = {cell.id}) as S{index}
                        on heroes_hero.id = S{index}.hero_id
                        """

        query += """
                        order by heroes_hero.id
                        """

        with psycopg2.connect(**conn_params) as conn:
            with conn.cursor() as cur:
                cur.execute(query)

                result = cur.fetchall()

        result.insert(0, (str(cell), ))

        total_result.extend(result)

    total_result.insert(0, ('id', 'Имя', 'Фамилия') + tuple(dates_repr))

    # [print(item) for item in total_result]

    """
    ('id', 'Имя', 'Фамилия', 'Sep01', 'Sep08', 'Sep15', 'Sep22')
(1, 'Андрей', 'Новиков', True, True, True, None)
(1, 'Андрей', 'Новиков', True, True, True, None)
(2, 'Тихон', 'Стафеев', True, True, True, None) 
(2, 'Тихон', 'Стафеев', True, True, True, None) 

"""

    image_filename = create_image(total_result)

    return image_filename


def get_attendance_2():
    """NOT USED.
    Want to do correct request by Django Model Objects.

    в статусе Героя есть ячейка и наставник """

    dates = get_4_last_training_dates("%Y-%m-%d")
    dates_repr = get_4_last_training_dates("%b%d")
    # id, hero, 4 dates
    zero_line = ['id', 'Имя', 'Фамилия'] + dates_repr
    my_data = [zero_line]

    """result = Training.objects.filter(date__in=dates)

    # [print(item) for item in result]



    for cell in Cell.objects.all():
        print(f'cell: {cell}')

        for hero in Hero.object.all():


        trainings = Training.objects.filter(date__in=dates, cell=cell)

        for training in trainings:
            print(f'date: {training.date}, heroes: {training.heroes.all()}')"""

    """for training in result:
        new_line = [f'{training.cell.location}, {training.date} {training.cell.day_time}']
        my_data.append(new_line)

        for hero in training.heroes.all():
            new_line = [hero.pk, hero.name, hero.surname]
            for date in dates:
                print(training.date)
                print(date)
                if training.date is date:
                    new_line.append(True)
                else:
                    new_line.append(False)
                print(new_line)
            my_data.append(new_line)"""

    image_filename = create_image(my_data)

    return image_filename
