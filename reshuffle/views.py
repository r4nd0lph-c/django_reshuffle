import os

from datetime import datetime

from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponseNotFound, FileResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView

from reshuffle.forms import *
from reshuffle.services.logic import get_time_create, DOCS_ROOT, ARCHIVE_NAME, ARCHIVE_LIFETIME


# Create your views here.


class Index(LoginRequiredMixin, TemplateView):
    """ CBV for main page """

    template_name = 'reshuffle/index.html'
    login_url = reverse_lazy('auth')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Выбор действия | RESHUFFLE'
        context['subtitle'] = 'Выберите действие'

        username = (self.request.user.first_name + ' ' + self.request.user.last_name).strip()
        if username == '':
            username = self.request.user.username
        context['footertext'] = {'label': 'Вы авторизовались как', 'username': username}

        return context


class Auth(LoginView):
    """ CBV for auth page """

    form_class = AuthForm

    template_name = 'reshuffle/auth.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация | RESHUFFLE'
        context['subtitle'] = 'Система создания тестов'
        context['footertext'] = 'Возникли проблемы?'

        return context

    def form_valid(self, form):
        remember_me = form.cleaned_data['remember_me']
        if not remember_me:
            self.request.session.set_expiry(0)
            self.request.session.modified = True
        return super(Auth, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('index')


class Creation(LoginRequiredMixin, FormView):
    """ CBV for creation page """

    form_class = CreationForm

    template_name = 'reshuffle/creation.html'
    login_url = reverse_lazy('auth')

    # success_url = reverse_lazy('download')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создание вариантов | RESHUFFLE'
        context['subtitle'] = 'Создать варианты'
        context['footertext'] = {'label': 'Вернуться на ', 'link': 'главную'}

        return context

    def form_valid(self, form):
        form.logic(self.request.user.username)
        # return super().form_valid(form)
        self.request.session['redirect_info'] = {'subj': form.cleaned_data['subject'].case_dative,
                                                 'amount': form.cleaned_data['amount']}
        return redirect(reverse_lazy('download'))


class Download(LoginRequiredMixin, TemplateView):
    """ CBV for download page """

    template_name = 'reshuffle/download.html'
    login_url = reverse_lazy('auth')

    def clean_trash(self):
        return logic.clean_trash(self.request.user.username)

    def get_context_data(self, *, object_list=None, **kwargs):
        is_cleaning = self.clean_trash()

        context = super().get_context_data(**kwargs)
        context['title'] = 'Скачать варианты | RESHUFFLE'
        context['subtitle'] = 'Скачайте варианты'
        context['footertext'] = {'label': 'Вернуться на ', 'link': 'главную'}
        context['is_cleaning'] = is_cleaning

        if not is_cleaning:
            archive = os.path.join(DOCS_ROOT, self.request.user.username, ARCHIVE_NAME + '.zip')
            time_create = get_time_create(archive)
            context['time_create'] = time_create.strftime('%H:%M %d.%m.%Y')

            time_exist = abs(datetime.now() - time_create).total_seconds() / 3600
            time_left = ARCHIVE_LIFETIME - time_exist
            if time_left > 1:
                context['time_left'] = '{} ч.'.format(round(time_left))
            elif time_left > 1 / 60:
                context['time_left'] = '{} мин.'.format(round(time_left * 60))
            else:
                context['time_left'] = '< 1 мин.'
        else:
            context['archive_lifetime'] = ARCHIVE_LIFETIME

        def ending(n):
            if str(n)[-1] == '1' and n != 11:
                return ''
            elif 2 <= int(str(n)[-1]) <= 4 and n not in [12, 13, 14]:
                return 'а'
            else:
                return 'ов'

        redirect_info = None
        if 'redirect_info' in self.request.session:
            subj = self.request.session['redirect_info']['subj']
            amount = self.request.session['redirect_info']['amount']
            del self.request.session['redirect_info']

            redirect_info = ['Создан{}'.format('' if str(amount)[-1] == '1' and amount != 11 else 'о'), amount,
                             'вариант{} по {}'.format(ending(amount), subj.lower())]

        context['redirect_info'] = redirect_info

        return context


def download_archive(request):
    """ download archive function that returns last created (with this user) archive """
    archive = os.path.join(DOCS_ROOT, request.user.username, ARCHIVE_NAME + '.zip')
    response = FileResponse(open(archive, 'rb'))
    return response


def logout_user(request):
    """ logout function with redirect to auth page """
    logout(request)
    return redirect('auth')


def page_not_found(request, exception):
    """ FBV for 404 error page """
    return HttpResponseNotFound('<h1>Страница не найдена [404]</h1>')
