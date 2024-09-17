from django.apps import AppConfig
from config.settings import RUN_POLLING
from time import sleep

class TelegramScheduleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'telegram_schedule'

    """def ready(self):
        if RUN_POLLING == 'TRUE':
            from telegram_schedule.services import start_polling
            sleep(1)
            start_polling()
            print('tg started')
        else:
            print('tg not started')"""