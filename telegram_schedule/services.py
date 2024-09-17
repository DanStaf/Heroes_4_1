from config.settings import TG_API_TOKEN

import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

from apscheduler.schedulers.background import BackgroundScheduler

import telebot


TOKEN = TG_API_TOKEN

# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")


@dp.message()
async def echo_handler(message: Message) -> None:

    try:
        # Send a copy of the received message
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer("Nice try! (your message is not supported)")


async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # And the run events dispatching
    await dp.start_polling(bot)


def start_polling():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())


##############


def start_scheduler(my_task, interval_sec):
    scheduler = BackgroundScheduler()

    if not scheduler.get_jobs():
        scheduler.add_job(my_task, 'interval', seconds=interval_sec)

    if not scheduler.running:
        scheduler.start()


def print_hello():
    print("HELLO")


def start_scheduler_hello():
    start_scheduler(print_hello, 10)


def good_morning():
    text = "Доброе утро!"
    print(text)

    # bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    bot = telebot.TeleBot(TG_API_TOKEN)
    bot.send_message(1816252417, text)


def start_scheduler_good_morning():
    scheduler = BackgroundScheduler()

    if not scheduler.get_jobs():
        scheduler.add_job(print_hello, 'interval', seconds=10)

    if not scheduler.running:
        scheduler.start()

