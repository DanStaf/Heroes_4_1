from users.models import User
from heroes.models import Team, Parent, Branch, Training
import datetime
from PIL import Image, ImageDraw, ImageFont
from config.settings import FONT_PATH, DATABASES
import psycopg2


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


def create_training(team_name, tg_id, date, heroes):

    user = User.objects.get(tg_id=tg_id)

    ### not good!
    mentor = Parent.objects.get(phone=user.phone)

    # 'team_name': 'Москва. Одинцово вс 09:00 Стафеев'
    split_text = team_name.split(' ')
    branch_dt = ' '.join(split_text[:-1])
    branch = Branch.objects.get(location=branch_dt[:-9])
    day_time = branch_dt[-8:]
    team_mentor = Parent.objects.get(surname=split_text[-1])

    # checked
    team = Team.objects.get(branch=branch, day_time=day_time, mentor=team_mentor)

    tr = Training.objects.create(mentor=mentor,
                                 date=get_date_format(date),
                                 team=team
                                 )
    tr.heroes.add(*heroes)
    tr.save()

    return len(heroes)


def get_date_format(text_date):

    # 'Значение “08.09.2024” должно быть в формате YYYY-MM-DD.'
    day = text_date[:2]
    mon = text_date[3:5]
    year = text_date[-4:]
    return year + '-' + mon + '-' + day


def get_attendance():
    """ use direct SQL request """

    dates = get_4_last_training_dates("%Y-%m-%d")
    dates_repr = get_4_last_training_dates("%b%d")

    conn_params = {
        "host": DATABASES['default']['HOST'],
        "database": DATABASES['default']['NAME'],
        "user": DATABASES['default']['USER'],
        "password": DATABASES['default']['PASSWORD']
    }

    teams = Team.objects.all()

    total_result = []

    for team in teams:

        query = """
                        SELECT
                        heroes_hero.id,
                        heroes_hero.name,
                        heroes_hero.surname"""

        for index, one_date_repr in enumerate(dates_repr):
            query += f""",
                        S{index}.training_date as {one_date_repr}"""

        query += """
                        from heroes_hero
                        """

        for index, one_date in enumerate(dates):
            query += f"""
                        FULL JOIN (SELECT
                          hero_id,
                          training_id,
                          true as training_date
                        FROM heroes_training_heroes A
                        INNER JOIN heroes_training T on A.training_id = T.id
                        WHERE T.date = '{one_date}' and T.team_id = {team.id}) as S{index}
                        on heroes_hero.id = S{index}.hero_id
                        """

        query += """
                        order by heroes_hero.id
                        """

        # ERROR - TeleBot: "Infinity polling exception: cannot open resource"
        # line 304, in chose_action image_filename = get_attendance()

        with psycopg2.connect(**conn_params) as conn:
            with conn.cursor() as cur:
                cur.execute(query)

                result = cur.fetchall()

        result.insert(0, (str(team), ))

        total_result.extend(result)

    total_result.insert(0, ('id', 'Имя', 'Фамилия') + tuple(dates_repr))

    # [print(item) for item in total_result]

    """
    ('id', 'Имя', 'Фамилия', 'Sep01', 'Sep08', 'Sep15', 'Sep22')
(1, 'Андрей', 'Новиков', True, True, True, None)
(1, 'Андрей', 'Новиков', True, True, True, None)
(2, 'Тихон', 'Стафеев', True, True, True, None) 
(2, 'Тихон', 'Стафеев', True, True, True, None) 

"""

    image_filename = create_image(total_result)

    return image_filename


#################


def get_attendance_2():
    """NOT USED.
    Want to do correct request by Django Model Objects.

    в статусе Героя есть ячейка и наставник """

    dates = get_4_last_training_dates("%Y-%m-%d")
    dates_repr = get_4_last_training_dates("%b%d")
    # id, hero, 4 dates
    zero_line = ['id', 'Имя', 'Фамилия'] + dates_repr
    my_data = [zero_line]

    """result = Training.objects.filter(date__in=dates)

    # [print(item) for item in result]



    for cell in Cell.objects.all():
        print(f'cell: {cell}')

        for hero in Hero.object.all():


        trainings = Training.objects.filter(date__in=dates, cell=cell)

        for training in trainings:
            print(f'date: {training.date}, heroes: {training.heroes.all()}')"""

    """for training in result:
        new_line = [f'{training.cell.location}, {training.date} {training.cell.day_time}']
        my_data.append(new_line)

        for hero in training.heroes.all():
            new_line = [hero.pk, hero.name, hero.surname]
            for date in dates:
                print(training.date)
                print(date)
                if training.date is date:
                    new_line.append(True)
                else:
                    new_line.append(False)
                print(new_line)
            my_data.append(new_line)"""

    image_filename = create_image(my_data)

    return image_filename
