from users.models import User
from heroes.models import Team, Parent
import datetime
from PIL import Image, ImageDraw, ImageFont
from config.settings import FONT_PATH


def create_new_user_mentor(message, phone, email):

    new_mentor = User.objects.create(tg_id=message.from_user.id,
                                     email=email,
                                     phone=phone,
                                     first_name=message.from_user.first_name,
                                     last_name=message.from_user.last_name)
    new_mentor.is_active = False
    new_mentor.set_password('12345')
    new_mentor.save()

    try:
        pa = Parent.objects.get(phone=phone)

    except Exception as e:

        # Пока добавляем только наставников, не вожатых.
        # Можно будет добавить пункт при регистрации.

        new_parent = Parent.objects.create(phone=phone,
                                           name=message.from_user.first_name,
                                           surname=message.from_user.last_name,
                                           sex=Parent.DAD)
        new_parent.save()


def user_set_staff(tg_id):
    user = User.objects.get(tg_id=tg_id)
    user.is_staff = True
    user.is_superuser = True

    user.save()


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


def get_teams():
    return [str(item) for item in Team.objects.all()]


def create_image(my_data: list):

    font_size = 15
    interval = 3
    fields = 20
    column_width = 70
    x_size = column_width * len(my_data[0]) + fields * 2
    y_size = len(my_data) * (font_size + interval) + fields * 2

    image = Image.new('RGB', (x_size, y_size), 'white')

    font = ImageFont.truetype(FONT_PATH, font_size)

    drawer = ImageDraw.Draw(image)
    y = fields
    for line in my_data:
        x = fields
        for cell in line:
            if cell is None:
                pass
            elif type(cell) is bool and cell == True:
                drawer.text((x, y), '+', font=font, fill='black')
            else:
                drawer.text((x, y), str(cell), font=font, fill='black')
            x += column_width
        y += font_size + interval

    time_stamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f'new_img_{time_stamp}.jpg'
    image.save(filename)

    return filename
