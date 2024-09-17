import datetime

from config.settings import TG_API_TOKEN
import telebot

from apscheduler.schedulers.background import BackgroundScheduler


def start_scheduler(my_task, interval_sec):
    scheduler = BackgroundScheduler()

    if not scheduler.get_jobs():
        scheduler.add_job(my_task, 'interval', seconds=interval_sec)

    if not scheduler.running:
        scheduler.start()


############


def print_hello():
    print("HELLO")


def start_scheduler_hello():
    start_scheduler(print_hello, 10)


def send_to_tg(chat_id, text):
    bot = telebot.TeleBot(TG_API_TOKEN)
    bot.send_message(1816252417, text)
    print(text)


def good_morning():
    send_to_tg(1816252417, f"Доброе утро! Сейчас {datetime.datetime.now()}")


def start_scheduler_good_morning():
    start_scheduler(good_morning, 60)


def send_poll_train():
    send_to_tg(1816252417, f"Опрос. Отметьте явку")


def send_poll_missed():
    send_to_tg(1816252417, f"Опрос. Кто предупредил, что пропустит?")


def chose_cell():
    send_to_tg(1816252417, f"В какую локацию завтра едете на тренировку? в Одинцово? кнопки да/нет")


def reminder_call_missed():
    send_to_tg(1816252417, f"Позвонить пропустившим тренировку! список")


def reminder_call_new():
    send_to_tg(1816252417, f"Позвонить новичкам! список")


def read_reply():
    bot = telebot.TeleBot(TG_API_TOKEN)
    bot.get_chat(1816252417)



def start_scheduler_mentor():

    scheduler = BackgroundScheduler()

    if not scheduler.get_jobs():
        scheduler.add_job(chose_cell, 'cron', day_of_week='sat', hour=20, minute=00)
        scheduler.add_job(send_poll_train, 'cron', day_of_week='sun', hour=8, minute=00)
        scheduler.add_job(send_poll_missed, 'cron', day_of_week='sun', hour=9, minute=00)
        scheduler.add_job(reminder_call_missed, 'cron', day_of_week='mon', hour=10, minute=00)
        scheduler.add_job(reminder_call_new, 'cron', day_of_week='tue', hour=10, minute=00)

    if not scheduler.running:
        scheduler.start()


def start_polling():
    bot = telebot.TeleBot(TG_API_TOKEN)
    bot.infinity_polling()


def get_updates():
    # telebot.apihelper.get_updates()
    bot = telebot.TeleBot(TG_API_TOKEN)
    res = bot.get_updates(-2)
    # ответ в формате update_id, message
    # параметр 869593995 - первый update_id, с которого нужно начинать читать

    [print(
        f"{item.message.text} from {item.message.chat.id} {item.message.from_user.username}"

    ) for item in res]
