from django.core.management import BaseCommand
from telegram_schedule.services import start_polling


class Command(BaseCommand):

    def handle(self, *args, **options):
        start_polling()
