from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from reshuffle.fields import LatexField


# Create your models here.


class Subjects(models.Model):
    case_nominative = models.CharField(max_length=32, verbose_name='Название')
    case_dative = models.CharField(max_length=32, verbose_name='Дательный падеж')
    tasks_number = models.SmallIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(100)],
                                            verbose_name='Количество заданий в варианте')

    def __str__(self):
        return str(self.case_nominative)

    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'
        ordering = ['id']


class Tasks(models.Model):
    subject_fk = models.ForeignKey(Subjects, on_delete=models.CASCADE, verbose_name='Ключ предмета')
    num = models.SmallIntegerField(default=1, validators=[MinValueValidator(1)], verbose_name='Номер задания в тесте')
    text = models.TextField(blank=True, verbose_name='Текст задания')
    latex = LatexField(blank=True, verbose_name='Формула (LaTeX)')
    image = models.ImageField(blank=True, upload_to='thumbnails_task/', verbose_name='Изображение')

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Задание'
        verbose_name_plural = 'Задания'
        ordering = ['subject_fk', 'num']


class Options(models.Model):
    task_fk = models.ForeignKey(Tasks, on_delete=models.CASCADE, verbose_name='Ключ задания')
    text = models.TextField(blank=True, verbose_name='Текст ответа')
    latex = LatexField(blank=True, verbose_name='Формула (LaTeX)')
    image = models.ImageField(blank=True, upload_to='thumbnails_option/', verbose_name='Изображение')
    is_answer = models.BooleanField(default=False, verbose_name='Верный ответ?')

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Вариант ответа'
        verbose_name_plural = 'Варианты ответов'
        ordering = ['task_fk', 'id']
