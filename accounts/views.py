import datetime

from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import render, redirect
from django.contrib import messages
from icecream import ic

from .forms import UserLoginForm, UserRegistrationForm, ClientForm
from .models import Client

User = get_user_model()


def logout_view(request):
    """Функция выхода"""

    logout(request)
    return redirect('home')


def login_view(request):
    """Функция для авторизации"""

    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        data = form.cleaned_data
        email = data.get('email')
        password = data.get('password')
        user = authenticate(request, email=email, password=password)
        login(request, user)
        return redirect('home')
    return render(request, 'accounts/login.html', {'form': form})


def add_client_birth_view(request):
    """Сохраняем форму с данными о клиентах"""
    form = ClientForm(request.POST or None)
    if form.is_valid():
        new_client = form.save(commit=False)
        data = form.cleaned_data
        check_client = Client.objects.filter(chart_id=data['chart_id'], first_name=data['first_name'])
        if check_client.exists():
            messages.error(request, 'Клиент уже существует в системе!!')
        else:
            new_client.save()
            messages.success(request, 'Клиент добавлен в систему.')
            return redirect('add')
    return render(request, 'add_birthday.html', {'form': form})


def register_view(request):
    """ Функция для создания нового пользователя """

    form = UserRegistrationForm(request.POST or None)
    if form.is_valid():
        new_user = form.save(commit=False)  # instans) commit=False-->исп для полного соединения с базой
        data = form.cleaned_data
        new_user.set_password(form.cleaned_data['password'])  # ЗАШИФРОВЫВАЕТ пароль
        new_user.save()
        messages.success(request, 'Пользователь добавлен в систему.')
        return render(request, 'accounts/registered.html',
                      {'new_user': new_user})
    return render(request, 'accounts/registration.html', {'form': form})


def delete_view(request):
    """Функция для удаления пользователя"""

    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            qs = User.objects.get(pk=user.pk)
            qs.delete()
            messages.error(request, 'Пользователь удалён :(')
    return redirect('home')
