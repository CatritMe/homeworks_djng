import random
import secrets

from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, UpdateView

from config.settings import EMAIL_HOST_USER
from users.forms import UserRegisterForm, UserProfileForm
from users.models import User

CHARS = '+-*!&$#?=@abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'


class UserDetailView(DetailView):
    """Просмотр информации о конкретном пользователе"""
    model = User


class UserCreateView(CreateView):
    """Создание пользователя"""
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        """Отправка письма с ссылкой верификации и добавление токена пользователю"""
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/email_confirm/{token}/'
        send_mail(
            subject='Подтверждение почты',
            message=f'Привет, перейди по ссылке для подтверждения почты {url}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email]
        )
        return super().form_valid(form)


class ProfileView(UpdateView):
    """Редактирование профиля пользователя"""
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')
    template_name = 'users/profile.html'

    def get_object(self, queryset=None):
        """Переход на редактирование того, под кем сессия"""
        return self.request.user


def email_verification(request, token):
    """Проверка верификации после регистрации"""
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))


def generate_new_password(request):
    """Смена пароля при входе (отправка автоматически сгенерированного пароля на почту)"""
    new_password = ''
    for i in range(10):
        new_password += random.choice(CHARS)
    if request.method == 'POST':
        email = request.POST['email']
        user = get_object_or_404(User, email=email)
        send_mail(
            subject='Новый пароль',
            message=f'Ваш новый пароль {new_password}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email]
        )
        user.set_password(new_password)
        user.save()
        return redirect(reverse('users:login'))
    return render(request, 'users/gen_password.html')
