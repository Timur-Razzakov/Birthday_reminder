import datetime

from django.contrib.auth import authenticate, login, logout, get_user_model
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from icecream import ic

from reminder_service.custom_validators import TEMPLATE_NAME
from .forms import UserLoginForm, ClientForm, CompanyDetailForm
from .models import Client, CompanyDetail

User = get_user_model()


def logout_view(request):
    """Функция выхода"""
    # logout(request)
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
    else:
        messages.error(request, 'Перепроверьте введённые данные')
    return render(request, 'accounts/login.html', {'form': form})


def add_client_view(request):
    """Сохраняем форму с данными о клиентах"""
    form = ClientForm(request.POST or None)
    if form.is_valid():
        new_client = form.save(commit=False)
        data = form.cleaned_data
        fullname = f"{data['last_name'] + ' ' + data['first_name'] + ' ' + data['father_name']}"
        check_client = Client.objects.filter(passport=data['passport'], full_name=fullname)
        if check_client.exists():
            messages.error(request, 'Клиент уже существует в системе!!')
        else:
            new_client.full_name = fullname
            new_client.save()
            messages.success(request, 'Клиент добавлен в систему.')
            return redirect('add_client')
    else:
        messages.error(request, 'Перепроверьте введённые данные')
    return render(request, 'accounts/add_birthday.html', {'form': form})


def update_client_view(request, id):
    """Обновление данных о клиенте"""
    get_client = Client.objects.get(id=id)

    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            get_client.first_name = data['first_name'],
            get_client.last_name = data['last_name'],
            get_client.father_name = data['father_name'],
            get_client.phone_number = data['phone_number'],
            get_client.date_of_birth = data['date_of_birth'],
            get_client.inter_passport = data['inter_passport'],
            get_client.passport = data['passport'],
            get_client.gender = data['gender'],
            get_client.address = data['address'],
            get_client.city = data['city'],
            get_client.channel = data['channel'],
            get_client.traveled = data['traveled'],
            fullname = f"{data['last_name'] + ' ' + data['first_name'] + ' ' + data['father_name']}"
            get_client.fullname = fullname
            get_client.save()
            messages.success(request, 'Данные изменены!!')
            return redirect('add_client')
        else:
            messages.error(request, 'Перепроверьте введённые данные')
    form = ClientForm(
        initial={'first_name': get_client.first_name,
                 'last_name': get_client.last_name,
                 'father_name': get_client.father_name,
                 'email': get_client.email,
                 'phone_number': get_client.phone_number,
                 'date_of_birth': get_client.date_of_birth,
                 'inter_passport': get_client.inter_passport,
                 'passport': get_client.passport,
                 'gender': get_client.gender,
                 'address': get_client.address,
                 'city': get_client.city,
                 'channel': get_client.channel,
                 'traveled': get_client.traveled,
                 })
    return render(request, "accounts/add_birthday.html",
                  {'form': form})


def add_company_info_view(request):
    """Сохраняем информацию о компании"""
    form = CompanyDetailForm
    if request.method == "POST":
        form = CompanyDetailForm(request.POST, request.FILES)
        print(form.is_valid())
        if form.is_valid():
            company = form.save(commit=False)
            data = form.cleaned_data
            print(data)
            check_company = CompanyDetail.objects.filter(name=data['name'])
            print(check_company)
            if check_company.exists():
                messages.error(request, 'Информация об этой компании уже существует!!')
            else:
                company.save()
                messages.success(request, 'Информация о компании  добавлена в систему.')
                return redirect('add_company')
        else:
            messages.error(request, 'Перепроверьте введённые данные')
    return render(request, 'accounts/company_detail.html', {'form': form})


def show_all_company_view(request):
    """Выводит все компании"""
    get_company = CompanyDetail.objects.all().order_by('id')
    paginator = Paginator(get_company, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'accounts/show_company_detail.html', {'object_list': page_obj})


def update_company_detail_view(request, id):
    """Обновляем данные об указанных компаниях"""
    get_company = CompanyDetail.objects.get(id=id)
    if request.method == 'POST':
        form = CompanyDetailForm(request.POST, request.FILES, instance=get_company)
        if form.is_valid():
            form.save()
            messages.success(request, 'Данные изменены!!')
            return redirect('show_company_detail')
    else:
        form = CompanyDetailForm(instance=get_company)
    context = {'form': form}
    return render(request, 'accounts/company_detail.html',
                  context)
