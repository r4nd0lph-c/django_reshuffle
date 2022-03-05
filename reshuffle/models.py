from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.auth.models import Group, User

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
        verbose_name_plural = '[3] Предметы'
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
        verbose_name_plural = '[1] Задания'
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
        verbose_name_plural = '[2] Варианты ответов'
        ordering = ['task_fk', 'id']


class SubjAccess(models.Model):
    group_id = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name='Ключ группы')
    subject_fk = models.ForeignKey(Subjects, on_delete=models.CASCADE, verbose_name='Ключ предмета')

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Право доступа к каталогу'
        verbose_name_plural = '[4] Права доступа к каталогу'
        ordering = ['group_id']


class ArchiveLogs(models.Model):
    action_time = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время')
    username = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    archive_info = models.CharField(max_length=255, verbose_name='Архив')
    action = models.CharField(max_length=255, verbose_name='Действие')

    def __str__(self):
        return str(self.action_time)

    class Meta:
        verbose_name = 'Элемент журнала'
        verbose_name_plural = '[5] Журнал действий'
        ordering = ['-action_time']
