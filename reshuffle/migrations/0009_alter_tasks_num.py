# Generated by Django 3.2.9 on 2022-03-14 08:22

import django.core.validators
from django.db import migrations
import reshuffle.fields


class Migration(migrations.Migration):

    dependencies = [
        ('reshuffle', '0008_alter_subjects_header_alter_subjects_parts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasks',
            name='num',
            field=reshuffle.fields.TestNumField(default=1, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Фактический номер задания'),
        ),
    ]