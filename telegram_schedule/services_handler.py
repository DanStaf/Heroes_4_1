from heroes.models import Hero
from users.models import User

from config.settings import TG_API_TOKEN
import telebot

bot = telebot.TeleBot(TG_API_TOKEN)


@bot.message_handler(commands=['start'])
def start_message(message):

    print(f'{message.from_user.username} (id {message.chat.id}) push START')

    try:
        response = User.objects.get(tg_id=message.from_user.id)
        msg = bot.send_message(message.chat.id, f'Привет, {response.first_name}')

        # text = f"Привет, {response[0][1]}"
        #connector.offer_next_actions(message)

    except Exception as e:
        msg = bot.send_message(message.chat.id, f'Привет, я бот Heroes-CRM. Давай знакомиться! Введите имя:')
        #bot.register_next_step_handler(msg, connector.fill_new_user_mentor)


@bot.message_handler(func=lambda message: True)
def text_messages(message):
    print(message.from_user.username, 'sent:', message.text)
    bot.send_message(message.chat.id, f'ОК')
    # connector.chose_action(message)


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
