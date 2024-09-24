from users.models import User
import datetime


def create_new_user_mentor(message):
    new_mentor = User.objects.create(tg_id=message.from_user.id,
                                     first_name=message.from_user.first_name,
                                     last_name=message.from_user.last_name)
    new_mentor.set_password('12345')


def get_4_last_training_dates(my_format="%d.%m.%Y"):
        today = datetime.datetime.now()
        wd = today.weekday()  # среда == 2

        if wd == 6:
            sunday = today
        else:
            sunday = today - datetime.timedelta(days=wd+1)

        sundays = [sunday]

        for i in range(3):
            sunday = sunday - datetime.timedelta(days=7)
            sundays.append(sunday)

        sundays.sort()

        return [item.strftime(my_format) for item in sundays]

