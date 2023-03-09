import datetime

from django.core.paginator import Paginator
from django.db.models import Q, CharField, Value
from django.db.models.functions import Concat
from django.shortcuts import render, redirect
from django.contrib import messages
from icecream import ic
from .forms import MailingCommerceOfferFrom, HolidayFrom
from accounts.models import Client, CompanyDetail

from accounts.forms import SearchClientForm
from .models import Holiday


# Create your views here.

def show_all_client_view(request):
    """Поиск клиентов"""
    form = SearchClientForm()
    return render(request, 'home.html', {'form': form})


def searchView(request):
    """Выводим список клиентов"""
    form = SearchClientForm()
    full_name = request.GET.get('full_name', None)
    city = request.GET.get('city', None)
    birthday = request.GET.get('date_of_birth', None)
    email = request.GET.get('email', None)
    phone_number = request.GET.get('phone_number', None)
    context = {'full_name': full_name, 'city': city,
               'birthday': birthday, 'email': email,
               'phone_number': phone_number, 'form': form}
    if full_name or city or birthday or email or phone_number:
        _filter = {}
        if full_name:
            _filter['full_name'] = full_name
        elif city:  # __iexact игнорит регистр
            _filter['city'] = city
        elif birthday:
            _filter['date_of_birth'] = birthday
        elif email:
            _filter['email'] = email
        else:
            _filter['phone_number'] = phone_number
        qs = Client.objects.filter(**_filter)
        paginator = Paginator(qs, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['object_list'] = page_obj
    return render(request, 'accounts/clients_list.html', context)


def add_mailing_view(request):
    """Сохраняем рассылку новых предложений"""
    form = MailingCommerceOfferFrom(request.POST, request.FILES)
    if form.is_valid():
        new_mailing = form.save()
        data = form.cleaned_data
        client_chart_id = Client.objects.get(chart_id=data['chart_id'])
        if client_chart_id:
            messages.error(request, 'Такой chart_id уже есть')
        else:
            new_mailing.save()
            messages.success(request, 'Коммерческое предложение сохранено.')
            return render(request, 'home.html', {'new_mailing': new_mailing})
    return render(request, 'add_mailing.html', {'form': form})


def add_holiday_view(request):
    """Добавляем праздники"""
    form = HolidayFrom(request.POST, request.FILES)
    if form.is_valid():
        holiday = form.save(commit=False)
        data = form.cleaned_data
        check_holiday = Holiday.objects.filter(name=data['name'])
        if check_holiday.exists():
            messages.error(request, 'Этот праздник уже есть в базе!!')
        else:
            holiday.save()
            messages.success(request, 'Праздник был добавлен!')
            return redirect('add_holiday')
    return render(request, 'add_holiday.html', {'form': form})


def update_client_view(request):
    pass
