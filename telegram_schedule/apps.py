from django.apps import AppConfig
from config.settings import RUN_TELEGRAM
from time import sleep


class TelegramScheduleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'telegram_schedule'

    def ready(self):
        if RUN_TELEGRAM == 'TRUE':
            from telegram_schedule.services import start_scheduler_updates
            sleep(1)
            start_scheduler_updates()
            print('tg started')
        else:
            print('tg not started')
