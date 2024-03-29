# Generated by Django 4.0 on 2022-03-07 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reshuffle', '0007_alter_subjects_header_alter_subjects_parts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subjects',
            name='header',
            field=models.JSONField(blank=True, null=True, verbose_name='Общая инструкция'),
        ),
        migrations.AlterField(
            model_name='subjects',
            name='parts',
            field=models.JSONField(blank=True, null=True, verbose_name='Деление на части'),
        ),
    ]
