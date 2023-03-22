from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404

from .forms import UserLoginForm, ClientForm, CompanyDetailForm
from .models import Client, CompanyDetail

User = get_user_model()
import logging

logger = logging.getLogger(__name__)


# logger.warning('fasdf')

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
    else:
        logger.warning('')
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
    return render(request, 'accounts/add_client.html', {'form': form})


def update_client_view(request, id):
    """Обновление данных о клиенте"""
    get_client = get_object_or_404(Client, id=id)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=get_client)
        if form.is_valid():
            get_client = form.save(commit=False)
            data = form.cleaned_data
            fullname = f"{data['last_name']} {data['first_name']} {data['father_name']}"
            get_client.full_name = fullname
            get_client.save()
            messages.success(request, 'Данные изменены!!')
            return redirect('add_client')
    else:
        form = ClientForm(instance=get_client)

    return render(request, "accounts/add_client.html",
                  {'form': form})


def add_company_info_view(request):
    """Сохраняем информацию о компании"""
    form = CompanyDetailForm
    if request.method == "POST":
        form = CompanyDetailForm(request.POST, request.FILES)
        if form.is_valid():
            company = form.save(commit=False)
            data = form.cleaned_data
            check_company = CompanyDetail.objects.filter(name=data['name'])
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
