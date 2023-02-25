import datetime

from django.shortcuts import render, redirect
from django.contrib import messages
from icecream import ic

from .forms import MailingCommerceOfferFrom
from accounts.models import Client, CompanyDetail


# Create your views here.

def show_all_client_birth_view(request):
    """Выводим всех клиентов и их дни рождения"""
    today = datetime.date.today()
    ic(today)
    client_chart_id = Client.objects.filter(date_of_birth=today)
    if client_chart_id:
        ic(client_chart_id),
    else:
        ic('error')
    return render(request, 'home.html')


def add_mailing_view(request):
    """Сохраняем рассылку новых предложений"""
    form = MailingCommerceOfferFrom(request.POST or None)
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


def add_holiday(request):
    pass
