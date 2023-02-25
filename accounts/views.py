import datetime

from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import render, redirect
from django.contrib import messages
from icecream import ic

from .forms import UserLoginForm, ClientForm, CompanyDetailForm
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
        check_client = Client.objects.filter(phone_number=data['phone_number'], first_name=data['first_name'])
        if check_client.exists():
            messages.error(request, 'Клиент уже существует в системе!!')
        else:
            new_client.save()
            messages.success(request, 'Клиент добавлен в систему.')
            return redirect('add_client')
    return render(request, 'accounts/add_birthday.html', {'form': form})


def add_company_info_view(request):
    """Сохраняем данные о компании"""
    form = CompanyDetailForm(request.POST or None)
    if form.is_valid():
        company = form.save(commit=False)
        data = form.cleaned_data
        check_company = Client.objects.filter(name=data['name'])
        if check_company.exists():
            messages.error(request, 'Информация об этой компании уже существует!!')
        else:
            company.save()
            messages.success(request, 'Информация о компании  добавлена в систему.')
            return redirect('accounts/add_company')
    return render(request, 'accounts/company_detail.html', {'form': form})

