from django.core.management import BaseCommand
# from telegram_schedule.services import get_updates, good_morning, start_polling
from telegram_schedule.services_handler import start_polling


class Command(BaseCommand):

    def handle(self, *args, **options):
        # get_updates()
        # good_morning()
        start_polling()
