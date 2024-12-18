from django.core.management import BaseCommand
from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        if not User.objects.filter(email='danstaf@mail.ru'):

            user = User.objects.create(
                email='danstaf@mail.ru',
                tg_id=111111,
                first_name='Admin',
                last_name='Admin',
                is_staff=True,
                is_superuser=True
            )

            user.set_password('admin')
            user.save()

            print("Superuser created")
        else:
            print("Superuser exist")
