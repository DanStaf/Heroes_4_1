from django.core.management import BaseCommand
from telegram_schedule.services import good_morning


class Command(BaseCommand):

    def handle(self, *args, **options):
        good_morning()
