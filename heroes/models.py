import datetime

from django.db import models


class Branch(models.Model):
    # branch отделение
    # при удалении не должны удаляться статусы и тренировки

    location = models.CharField(max_length=50, verbose_name='Город (локация)')
    head = models.ForeignKey("heroes.Parent", verbose_name='Старший', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.location}'

    class Meta:
        verbose_name = 'отделение'
        verbose_name_plural = 'отделения'


class Team(models.Model):
    # team отряд
    # при удалении не должны удаляться статусы и тренировки

    DT_CHOICES = [
        ("сб 09:00", "сб 09:00"),
        ("сб 15:00", "сб 15:00"),
        ("вс 09:00", "вс 09:00"),
        ("вс 15:00", "вс 15:00"),
    ]

    TEAM_CHOICES = [
        ("Мощный", "Мощный"),
        ("Отважный", "Отважный"),
        ("Отряд мам", "Отряд мам"),
        ("Пред.командир", "Пред.командир"),
        ("Командир", "Командир"),
        ("Выбыл", "Выбыл"),
    ]

    branch = models.ForeignKey(Branch, verbose_name='Отделение', on_delete=models.SET_NULL, null=True, blank=True)
    day_time = models.CharField(max_length=50, choices=DT_CHOICES, verbose_name='Дата и время тренировки')
    mentor = models.ForeignKey("heroes.Parent", verbose_name='Наставник/Вожатая', on_delete=models.SET_NULL, null=True, blank=True)
    type = models.CharField(max_length=50, choices=TEAM_CHOICES, verbose_name='Вид отряда')

    def __str__(self):
        return f'{self.branch} {self.day_time} {self.mentor.surname}'

    class Meta:
        verbose_name = 'отряд'
        verbose_name_plural = 'отряды'


"""class Cell(models.Model):
    # branch отделение
    # team отряд / troop, group, band, , unit

    # при удалении ячейки удалены статусы и тренировки

    DT_CHOICES = [
        ("сб 09:00", "сб 09:00"),
        ("сб 15:00", "сб 15:00"),
        ("вс 09:00", "вс 09:00"),
        ("вс 15:00", "вс 15:00"),
    ]

    location = models.CharField(max_length=50, verbose_name='Город (локация)')
    day_time = models.CharField(max_length=50, choices=DT_CHOICES, verbose_name='Дата и время тренировки')

    def __str__(self):
        return f'{self.location} {self.day_time}'

    class Meta:
        verbose_name = 'ячейка'
        verbose_name_plural = 'ячейки'
"""


class Parent(models.Model):
    """
feedback boolean, -- отзыв?
"""

    DAD = "Папа"
    MOM = "Мама"
    GR_M = "Бабушка"
    GR_F = "Дедушка"
    MOTHER_IN_CLASS = "Вожатая класса"

    PARENT_CHOICES = [
        (DAD, "Папа"),
        (MOM, "Мама"),
        (GR_M, "Бабушка"),
        (GR_F, "Дедушка"),
        (MOTHER_IN_CLASS, "Вожатая класса")
    ]

    name = models.CharField(max_length=50, verbose_name='Имя')
    surname = models.CharField(max_length=50, verbose_name='Фамилия')
    sex = models.CharField(max_length=50, choices=PARENT_CHOICES, default=MOM, verbose_name='Пол')
    phone = models.PositiveBigIntegerField(verbose_name='Телефон')

    def __str__(self):
        return f'{self.sex}: {self.name} {self.surname}'

    class Meta:
        verbose_name = 'родитель'
        verbose_name_plural = 'родители'


class Hero(models.Model):
    """
new boolean,
first_training_date date,
planned_first_training_date date,
profile boolean, -- анкета
photo
"""

    BOY = "Мальчик"
    GIRL = "Девочка"

    HERO_CHOICES = [
        (BOY, "Мальчик"),
        (GIRL, "Девочка")
    ]

    name = models.CharField(max_length=50, verbose_name='Имя')
    surname = models.CharField(max_length=50, verbose_name='Фамилия')
    sex = models.CharField(max_length=50, choices=HERO_CHOICES, verbose_name='Пол')
    birth_date = models.DateField(verbose_name='Дата рождения')
    phone = models.PositiveBigIntegerField(verbose_name='Телефон', null=True, blank=True)

    parents = models.ManyToManyField(Parent, verbose_name='Родители')

    def __str__(self):
        return f'Герой: {self.name} {self.surname}'

    class Meta:
        verbose_name = 'герой'
        verbose_name_plural = 'герои'


class ParentStatus(models.Model):

    PROGRAM_CHOICES = [
        ("Сила Дружбы", "Сила Дружбы"),
        ("Школа Мам", "Школа Мам"),
        ("Институт", "Институт"),
        ("Вожатая", "Вожатая"),
        ("Гостевой", "Гостевой"),
        ("Выбыли", "Выбыли"),
        ("Наставник", "Наставник"),
        ("Стажёр", "Стажёр"),
        ("Интересуется", "Интересуется"),
        ("Не интересуется", "Не интересуется"),
    ]

    parent = models.ForeignKey(Parent, verbose_name='Родитель', on_delete=models.CASCADE)
    type = models.CharField(max_length=50, choices=PROGRAM_CHOICES, verbose_name='Вид программы')
    start_from = models.DateField(verbose_name='с')
    stop_at = models.DateField(verbose_name='по', null=True, blank=True)
    branch = models.ForeignKey(Branch, verbose_name='Отделение', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.parent} ({self.type}) {"+" if self.is_active() else "-"}'

    def is_active(self):
        today = datetime.datetime.now().date()
        return (self.start_from < today) and (self.stop_at is None)

    class Meta:
        verbose_name = 'статус родителя'
        verbose_name_plural = 'статусы родителей'


class HeroStatus(models.Model):

    hero = models.ForeignKey(Hero, verbose_name='Герой', on_delete=models.CASCADE)
    start_from = models.DateField(verbose_name='с')
    stop_at = models.DateField(verbose_name='по', null=True, blank=True)
    team = models.ForeignKey(Team, verbose_name='Отряд', on_delete=models.SET_NULL, null=True, blank=True)
    # mentor = models.ForeignKey(Parent, verbose_name='Наставник', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.hero} ({self.team.type}) {"+" if self.is_active() else "-"}'

    def is_active(self):
        today = datetime.datetime.now().date()
        return (self.start_from < today) and (self.stop_at is None)

    class Meta:
        verbose_name = 'статус героя'
        verbose_name_plural = 'статусы героев'


class Training(models.Model):

    mentor = models.ForeignKey(Parent, verbose_name='Наставник', on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField(verbose_name='Дата тренировки')
    team = models.ForeignKey(Team, verbose_name='Отряд', on_delete=models.SET_NULL, null=True, blank=True)

    heroes = models.ManyToManyField(Hero, verbose_name='Явка героев')

    # comments ?

    def __str__(self):
        return f'Тренировка: {self.date} {self.team}'

    class Meta:
        verbose_name = 'тренировка'
        verbose_name_plural = 'тренировки'


class PaymentType(models.Model):

    title = models.CharField(max_length=50, verbose_name='Вид платежа')
    value = models.PositiveIntegerField(verbose_name='Стоимость')

    # comments ?

    def __str__(self):
        return f'Абонемент: {self.title} ({self.value} р.)'

    class Meta:
        verbose_name = 'абонемент'
        verbose_name_plural = 'абонементы'


class Payment(models.Model):

    parent = models.ForeignKey(Parent, verbose_name='Родитель', on_delete=models.CASCADE)
    date = models.DateField(verbose_name='Дата оплаты')
    type = models.ForeignKey(PaymentType, verbose_name='Вид платежа', on_delete=models.CASCADE)

    # comments ?

    def __str__(self):
        return f'Оплата: {self.parent} {self.date}'

    class Meta:
        verbose_name = 'платёж'
        verbose_name_plural = 'платежи'
