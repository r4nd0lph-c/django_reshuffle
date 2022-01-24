from django import forms
from django.contrib.auth.forms import AuthenticationForm

from reshuffle.models import Subjects, ArchiveLogs
from reshuffle.services import logic


class AuthForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя',
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '*'}))
    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput(
                                   attrs={'class': 'form-control', 'placeholder': '*', 'style': 'border-right:0px;'}))
    remember_me = forms.BooleanField(label='Запомнить меня?', required=False, initial=True,
                                     widget=forms.CheckboxInput(
                                         attrs={'class': 'form-check-input me-1', 'type': 'checkbox'}))


class CreationForm(forms.Form):
    amount_min = 1
    amount_max = 100
    subject = forms.ModelChoiceField(queryset=Subjects.objects.all(), label='Предмет', empty_label='Выберите предмет',
                                     widget=forms.Select(attrs={'class': 'form-select custom_padding'}))
    amount = forms.IntegerField(label='Количество вариантов', min_value=amount_min, max_value=amount_max,
                                widget=forms.NumberInput(
                                    attrs={'type': 'range', 'class': 'form-range',
                                           'oninput': 'this.previousElementSibling.value = this.value',
                                           'value': amount_min, 'min': amount_min, 'max': amount_max}))

    @staticmethod
    def add_logs_creation(user, arch_info):
        ArchiveLogs.objects.create(username=user,
                                   archive_info='Архив по {} [{}]'.format(arch_info['subj'], arch_info['amount']),
                                   action='Создание')

    def logic(self, username):
        logic.main(self.cleaned_data, username)
