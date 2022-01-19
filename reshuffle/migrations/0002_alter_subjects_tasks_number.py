# Generated by Django 4.0 on 2022-01-01 15:38

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reshuffle', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subjects',
            name='tasks_number',
            field=models.SmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)], verbose_name='Количество заданий в варианте'),
        ),
    ]
