from django.core.management import BaseCommand
from telegram_schedule.services import get_updates, good_morning


class Command(BaseCommand):

    def handle(self, *args, **options):
        get_updates()
        # good_morning()
