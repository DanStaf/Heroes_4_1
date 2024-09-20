from heroes.models import Hero
from users.models import User

# from services_connector import fill_new_user_mentor

from config.settings import TG_API_TOKEN
import telebot

bot = telebot.TeleBot(TG_API_TOKEN)


@bot.message_handler(commands=['start'])
def start_message(message):

    # print(f'{message.from_user.username} (id {message.chat.id}) push START')

    try:
        response = User.objects.get(tg_id=message.from_user.id)
        msg = bot.send_message(message.chat.id, f'Привет, {response.first_name}')

    except Exception as e:
        create_new_user_mentor(message)
        msg = bot.send_message(message.chat.id, f'Привет {message.from_user.first_name}, я бот Heroes-CRM. Внёс тебя в базу.')

    offer_next_actions(message)


@bot.message_handler(func=lambda message: True)
def text_messages(message):
    print(message.from_user.username, 'sent:', message.text)
    #bot.send_message(message.chat.id, f'ОК')
    chose_action(message)


@bot.poll_answer_handler()
def handle_poll_answer(poll_answer):
    # connector.user_poll_input(poll_answer)
    bot.send_message(poll_answer.chat.id, f'ОК')




"""@bot.message_handler()
def send_welcome(message):

    my_heroes = Hero.objects.all()
    my_text = f"Hi! Your message: {message.text}\n My heroes: "

    for hero in my_heroes:
        my_text += f"\n {hero}"

    msg = bot.reply_to(message, my_text)
"""


def start_polling():
    bot.infinity_polling()


##############


def create_new_user_mentor(message):
    new_mentor = User.objects.create(tg_id=message.from_user.id,
                                     first_name=message.from_user.first_name,
                                     last_name=message.from_user.last_name)
    new_mentor.set_password('12345')


def offer_next_actions(message):

    msg = bot.send_message(message.chat.id,
                           "Выбери действие:",
                           reply_markup=add_options_keyboard())

    bot.register_next_step_handler(msg, chose_action)


def add_options_keyboard(next_key=None):

    if next_key is None:
        buttons = ["Добавить маму или папу",
                   "Добавить героя",
                   "Добавить новичка",
                   "Добавить наставника или вожатую",
                   "Добавить продукт",
                   "Добавить платёж",
                   "Добавить ячейку",
                   "Отметить явку",
                   "Посмотреть явку",
                   "Посмотреть всех людей"
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
        # buttons = self.get_4_last_training_dates()
        buttons = None
    else:
        buttons = None

    if buttons is not None:
        keyboard = get_reply_keyboard(buttons)
        return keyboard
    else:
        return None


def chose_action(message):

        print('action:', message.text)
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

            """msg = bot.send_message(message.chat.id,
                                        f'Выберите дату:',
                                        reply_markup=add_options_keyboard("date_"))

            bot.register_next_step_handler(msg, start_attendance_poll)

            flag = False"""
            bot.send_message(message.chat.id, "Действие пока не реализовано")

        elif message.text == 'Посмотреть явку':

            bot.send_message(message.chat.id, "Действие пока не реализовано")

            """image_filename = get_attendance()
            text = 'Раз, два, три, ура!'

            with open(image_filename, 'rb') as img:

                msg = bot.send_photo(message.chat.id,
                                          photo=img,
                                          caption=text)

            os.remove(image_filename)

            flag = False"""

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
