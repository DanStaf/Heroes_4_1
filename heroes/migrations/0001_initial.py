# Generated by Django 5.1.1 on 2024-09-17 19:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cell',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=50, verbose_name='Город (локация)')),
                ('day_time', models.CharField(choices=[('сб 09:00', 'сб 09:00'), ('сб 15:00', 'сб 15:00'), ('вс 09:00', 'вс 09:00'), ('вс 15:00', 'вс 15:00')], max_length=50, verbose_name='Дата и время тренировки')),
            ],
            options={
                'verbose_name': 'ячейка',
                'verbose_name_plural': 'ячейки',
            },
        ),
        migrations.CreateModel(
            name='Hero',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Имя')),
                ('surname', models.CharField(max_length=50, verbose_name='Фамилия')),
                ('sex', models.CharField(choices=[('Мальчик', 'Мальчик'), ('Девочка', 'Девочка')], max_length=50, verbose_name='Пол')),
                ('birth_date', models.DateField(verbose_name='Дата рождения')),
            ],
            options={
                'verbose_name': 'герой',
                'verbose_name_plural': 'герои',
            },
        ),
        migrations.CreateModel(
            name='Parent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Имя')),
                ('surname', models.CharField(max_length=50, verbose_name='Фамилия')),
                ('sex', models.CharField(choices=[('Папа', 'Папа'), ('Мама', 'Мама'), ('Бабушка', 'Бабушка'), ('Дедушка', 'Дедушка'), ('Вожатая класса', 'Вожатая класса')], default='Мама', max_length=50, verbose_name='Пол')),
                ('phone', models.PositiveBigIntegerField(verbose_name='Телефон')),
            ],
            options={
                'verbose_name': 'родитель',
                'verbose_name_plural': 'родители',
            },
        ),
        migrations.CreateModel(
            name='PaymentType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Вид платежа')),
                ('value', models.PositiveIntegerField(verbose_name='Стоимость')),
            ],
            options={
                'verbose_name': 'абонемент',
                'verbose_name_plural': 'абонементы',
            },
        ),
        migrations.CreateModel(
            name='HeroStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('Мощный', 'Мощный'), ('Отважный', 'Отважный'), ('Отряд мам', 'Отряд мам'), ('Пред.командир', 'Пред.командир'), ('Командир', 'Командир'), ('Выбыл', 'Выбыл')], max_length=50, verbose_name='Вид отряда')),
                ('start_from', models.DateField(verbose_name='с')),
                ('stop_at', models.DateField(blank=True, null=True, verbose_name='по')),
                ('cell', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='heroes.cell', verbose_name='Ячейка')),
                ('hero', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='heroes.hero', verbose_name='Герой')),
                ('mentor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='heroes.parent', verbose_name='Наставник')),
            ],
            options={
                'verbose_name': 'статус героя',
                'verbose_name_plural': 'статусы героев',
            },
        ),
        migrations.AddField(
            model_name='hero',
            name='parents',
            field=models.ManyToManyField(to='heroes.parent', verbose_name='Родители'),
        ),
        migrations.CreateModel(
            name='ParentStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('Сила Дружбы', 'Сила Дружбы'), ('Школа Мам', 'Школа Мам'), ('Институт', 'Институт'), ('Вожатая', 'Вожатая'), ('Гостевой', 'Гостевой'), ('Выбыли', 'Выбыли'), ('Наставник', 'Наставник'), ('Стажёр', 'Стажёр'), ('Интересуется', 'Интересуется'), ('Не интересуется', 'Не интересуется')], max_length=50, verbose_name='Вид программы')),
                ('start_from', models.DateField(verbose_name='с')),
                ('stop_at', models.DateField(blank=True, null=True, verbose_name='по')),
                ('cell', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='heroes.cell', verbose_name='Ячейка')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='heroes.parent', verbose_name='Родитель')),
            ],
            options={
                'verbose_name': 'статус родителя',
                'verbose_name_plural': 'статусы родителей',
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Дата оплаты')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='heroes.parent', verbose_name='Родитель')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='heroes.paymenttype', verbose_name='Вид платежа')),
            ],
            options={
                'verbose_name': 'платёж',
                'verbose_name_plural': 'платежи',
            },
        ),
        migrations.CreateModel(
            name='Training',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Дата тренировки')),
                ('cell', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='heroes.cell', verbose_name='Ячейка')),
                ('heroes', models.ManyToManyField(to='heroes.hero', verbose_name='Явка героев')),
                ('mentor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='heroes.parent', verbose_name='Наставник')),
            ],
            options={
                'verbose_name': 'тренировка',
                'verbose_name_plural': 'тренировки',
            },
        ),
    ]
