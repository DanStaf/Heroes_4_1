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
