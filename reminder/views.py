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
    date_of_birth = request.GET.get('date_of_birth', '')
    email = request.GET.get('email', None)
    phone_number = request.GET.get('phone_number', None)
    context = {'full_name': full_name, 'city': city,
               'email': email, 'date_of_birth': date_of_birth,
               'phone_number': phone_number, 'form': form}
    if full_name or city or email or phone_number or date_of_birth:
        _filter = {}
        if full_name:  # __icontains --> поиск по части слова
            _filter['full_name__icontains'] = full_name
        if city:  # __iexact игнорит регистр
            _filter['city'] = city
        if date_of_birth:
            _filter['date_of_birth'] = date_of_birth
        if email:
            _filter['email'] = email
        if phone_number:
            _filter['phone_number'] = phone_number
        qs = Client.objects.filter(**_filter)
        paginator = Paginator(qs, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['object_list'] = page_obj
    return render(request, 'clients_list.html', context)


def add_mailing_view(request):
    """Сохраняем рассылку новых предложений"""
    form = MailingCommerceOfferFrom
    if request.method == "POST":
        form = MailingCommerceOfferFrom(request.POST, request.FILES)
        if form.is_valid():
            new_mailing = form.save(commit=False)
            new_mailing.save()
            messages.success(request, 'Коммерческое предложение сохранено.')
            return redirect('add_mailing')
    return render(request, 'add_mailing.html', {'form': form})


def add_holiday_view(request):
    """Добавляем праздники"""
    form = HolidayFrom
    if request.method == "POST":
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
