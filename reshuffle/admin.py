from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe

from .views import *
from .models import *
from .widgets import LatexInput


# Register your models here.


class SubjectsAdmin(admin.ModelAdmin):
    list_display = ('id', 'case_nominative', 'tasks_number')
    list_display_links = ('id', 'case_nominative')


class TasksForm(forms.ModelForm):
    def clean(self):
        if 'num' in self.cleaned_data:
            num = self.cleaned_data['num']
            if 'subject_fk' in self.cleaned_data:
                subj_id = self.cleaned_data['subject_fk'].id
                t_num = Subjects.objects.get(id=subj_id).tasks_number
                if num <= t_num:
                    if self.cleaned_data['text'] == '' and self.cleaned_data['latex'] == '' \
                            and (self.cleaned_data['image'] is None or self.cleaned_data['image'] is False):
                        raise forms.ValidationError({
                            'text': 'Хотя бы одно из полей "{}", "{}", "{}" должно быть заполнено.'.format(
                                Tasks._meta.get_field('text').verbose_name,
                                Tasks._meta.get_field('latex').verbose_name,
                                Tasks._meta.get_field('image').verbose_name)})
                else:
                    raise forms.ValidationError(
                        {'num': 'Убедитесь, что это значение меньше либо равно {}.'.format(t_num)})
            else:
                raise forms.ValidationError(
                    {'num': 'Для начала укажите "{}".'.format(Tasks._meta.get_field('subject_fk').verbose_name)})
        else:
            raise forms.ValidationError({'num': 'Убедитесь, что вы заполнили это поле.'})


class TasksAdmin(admin.ModelAdmin):
    form = TasksForm

    list_display = ('id', 'subject_fk', 'num', 'text', 'latex', 'get_html_img')
    list_display_links = ('id',)
    list_filter = ('subject_fk',)
    search_fields = ('=num',)

    formfield_overrides = {
        LatexField: {'widget': LatexInput},
    }

    def get_html_img(self, object):
        if object.image:
            return mark_safe('<img src="{}" style="max-width:100%">'.format(object.image.url))

    get_html_img.short_description = 'Изображение'


class OptionsForm(forms.ModelForm):
    def clean(self):
        if self.cleaned_data['text'] == '' and self.cleaned_data['latex'] == '' \
                and (self.cleaned_data['image'] is None or self.cleaned_data['image'] is False):
            raise forms.ValidationError({
                'text': 'Хотя бы одно из полей "{}", "{}", "{}" должно быть заполнено.'.format(
                    Tasks._meta.get_field('text').verbose_name,
                    Tasks._meta.get_field('latex').verbose_name,
                    Tasks._meta.get_field('image').verbose_name)})


class OptionsAdmin(admin.ModelAdmin):
    form = OptionsForm

    list_display = ('id', 'task_fk', 'text', 'latex', 'get_html_img', 'is_answer')
    list_display_links = ('id',)
    list_filter = ('task_fk__subject_fk',)
    search_fields = ('task_fk__id',)
    raw_id_fields = ('task_fk',)

    # autocomplete_fields = ['task_fk']

    formfield_overrides = {
        LatexField: {'widget': LatexInput},
    }

    def get_html_img(self, object):
        if object.image:
            return mark_safe('<img src="{}" style="max-width:100%">'.format(object.image.url))

    get_html_img.short_description = 'Изображение'


admin.site.register(Subjects, SubjectsAdmin)
admin.site.register(Tasks, TasksAdmin)
admin.site.register(Options, OptionsAdmin)

admin.site.site_title = 'RESHUFFLE'
admin.site.site_header = 'RESHUFFLE'
admin.site.index_title = 'Администрирование приложения'

admin.site.login = Auth.as_view()
admin.site.logout = logout_user
