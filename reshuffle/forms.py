from django import forms
from django.contrib.auth.forms import AuthenticationForm

from reshuffle.models import Subjects, ArchiveLogs, SubjAccess
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


def get_subj_queryset(user):
    qs = Subjects.objects.all()
    groups = user.groups.all()
    if not groups.exists() or user.is_superuser:
        return qs
    else:
        access_list = []
        for group in groups:
            qs_subj = SubjAccess.objects.filter(group_id=group.id)
            for item in qs_subj:
                access_list.append(item.subject_fk_id)
        return qs.filter(id__in=access_list)


class CreationForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.qs_subj = get_subj_queryset(self.user)
        super(CreationForm, self).__init__(*args, **kwargs)
        self.fields['subject'].queryset = self.qs_subj

    amount_min = 1
    amount_max = 300
    subject = forms.ModelChoiceField(queryset=None, label='Предмет', empty_label='Выберите предмет',
                                     widget=forms.Select(attrs={'class': 'form-select custom_padding'}))
    amount = forms.IntegerField(label='Количество вариантов:',
                                min_value=amount_min, max_value=amount_max,
                                widget=forms.NumberInput(
                                    attrs={'type': 'number', 'class': 'form-control custom_padding',
                                           'oninput': 'this.previousElementSibling.value = this.value',
                                           'value': amount_min, 'min': amount_min, 'max': amount_max}))

    @staticmethod
    def add_logs_creation(user, arch_info):
        ArchiveLogs.objects.create(username=user,
                                   archive_info='Архив по {} [{}]'.format(arch_info['subj'], arch_info['amount']),
                                   action='Создание')

    def logic(self, username):
        logic.main(self.cleaned_data, username)
