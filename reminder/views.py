import asyncio
import os
from io import BytesIO

from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from icecream import ic
from asgiref.sync import async_to_sync
from accounts.forms import SearchClientForm
from accounts.models import Client, CompanyDetail
from .tasks import send_messages
from .forms import MailingCommerceOfferFrom, HolidayFrom
from .models import Holiday, MailingCommerceOffer, TemplateForChannel, MultipleImage

from jinja2 import Template

from telegram_bot.user_bot import send_message_mailing


# Create your views here.

def show_all_client_view(request):
    """Поиск клиентов"""

    form = SearchClientForm()
    return render(request, 'home.html', {'form': form})


def searchView(request):
    """выводит список клиентов"""
    form = SearchClientForm()
    full_name = request.GET.get('full_name', None)
    city = request.GET.get('city', None)
    date_of_birth = request.GET.get('date_of_birth', '')
    email = request.GET.get('email', None)
    phone_number = request.GET.get('phone_number', None)
    context = {'full_name': full_name, 'city': city,
               'email': email, 'date_of_birth': date_of_birth,
               'phone_number': phone_number, 'form': form}
    if full_name or date_of_birth or city or email or phone_number:
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
        qs = Client.objects.filter(**_filter).order_by('date_of_birth')
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
            for image in request.FILES.getlist('images'):
                name = MultipleImage.objects.create(image=image)
                new_mailing.photo.add(MultipleImage.objects.get(image=name))
            new_mailing.save()
            form.save_m2m()
            messages.success(request, 'Коммерческое предложение сохранено.')
            return redirect('add_mailing')
        else:
            messages.error(request, 'Перепроверьте введённые данные')
    return render(request, 'add_mailing.html', {'form': form})


def show_mailings_view(request):
    get_mailings = MailingCommerceOffer.objects.all().order_by('sending_status')
    paginator = Paginator(get_mailings, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'show_mailing.html', {'object_list': page_obj})


def update_mailing_view(request, id):
    """Обновляем данные о коммерческом предложением"""
    mailing = MailingCommerceOffer.objects.get(id=id)
    if request.method == 'POST':
        form = MailingCommerceOfferFrom(request.POST, request.FILES, instance=mailing)
        if form.is_valid():
            # проверяем, если мы фото передали, то обновляем, если нет, то оставляем как есть
            if request.FILES.getlist('images'):
                mailing = form.save(commit=False)
                mailing.photo.clear()  # удаляем связи многие-ко-многим со старыми изображениями
                for image in request.FILES.getlist('images'):  # добавляем новые изображения
                    image_model = MultipleImage.objects.create(image=image)
                    mailing.photo.add(image_model)
            mailing.save()
            messages.success(request, 'Данные изменены!!')
            return redirect('show_mailings')
    else:
        form = MailingCommerceOfferFrom(instance=mailing)
    context = {'form': form}
    return render(request, "add_mailing.html",
                  context)


def send_mailing_view(request, id):
    api_id = os.environ.get('API_ID')
    api_hash = os.environ.get('API_HASH')
    """Отправляем указанное коммерческое предложение"""
    if request.user.is_authenticated:  # будет исп для выбора кому отправлять отчёт об отправке сообщений
        user = request.user
        mailing = MailingCommerceOffer.objects.get(id=id)
        if request.method == 'GET':
            template = TemplateForChannel.objects.get(name__icontains='предложение')
            if mailing.city is None:
                clients = Client.objects.all().values('phone_number', 'first_name')
            else:
                clients = Client.objects.filter(city=mailing.city).values('phone_number', 'first_name')
            mailing_message = Template(template.templates_for_massage)
            company_data = CompanyDetail.objects.filter(name=mailing.company_detail).values(
                'address',
                'name',
                'phone_number',
                'email',
                'web_site',
                'company_motto',
                'logo')
            image_data = []
            # проверяем, есть ли фотографии
            if mailing.photo:
                for item in mailing.photo.all():
                    image_data.append(item)
            # перебираем информацию о компании для template
            for item in company_data:
                msg = mailing_message.render(
                    message=mailing.message,
                    link=mailing.link,
                    name=item['name'],
                    address=item['address'],
                    phone_number=item['phone_number'],
                    email=item['email'],
                    web_site=item['web_site'],
                    company_motto=item['company_motto'],
                    logo=item['logo'],
                )
            # send_messages.delay(api_id, api_hash, mailing.id,
            #                     clients, msg, 'Razzakov_Timur')
            asyncio.run(send_message_mailing(api_id, api_hash, image_data, mailing.id,
                                             clients, msg, 'Razzakov_Timur'))
        messages.success(request, 'Успешно отправлено!!')
    return redirect('show_mailings')


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
                form.save_m2m()
                messages.success(request, 'Праздник был добавлен!')
                return redirect('add_holiday')
        else:
            messages.error(request, 'Перепроверьте введённые данные')

    return render(request, 'add_holiday.html', {'form': form})


def show_holiday_view(request):
    get_holidays = Holiday.objects.all().order_by('date')
    paginator = Paginator(get_holidays, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'show_holiday.html', {'object_list': page_obj})


def update_holiday_view(request, id):
    """Обновляем данные о празднике"""
    holiday = Holiday.objects.get(id=id)
    if request.method == 'POST':
        form = HolidayFrom(request.POST, request.FILES, instance=holiday)
        if form.is_valid():
            form.save()
            messages.success(request, 'Данные изменены!!')
            return redirect('show_holiday')
    else:
        form = HolidayFrom(instance=holiday)
    context = {'form': form}
    return render(request, "add_holiday.html",
                  context)
