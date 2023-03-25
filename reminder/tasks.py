import asyncio
import logging

from django.core.exceptions import ObjectDoesNotExist
from jinja2 import Template

from accounts.models import Client, CompanyDetail
from congratulations.check_birthday import birthday
from congratulations.check_holiday import holiday
from congratulations.delete_old_data import Command
from reminder.models import MailingCommerceOffer, TemplateForChannel, Result
from reminder_service.celery import app
from telegram_bot.user_bot import send_message_mailing, send_message_holiday

logger = logging.getLogger(__name__)


def get_data_from_result():
    """Получаем данные из модели Result"""
    data = Result.objects.filter(sending_status=False).values('id', 'client', 'process_date', 'message',
                                                              'sending_status')
    client_phones = []

    for item in data:
        all_phones = Client.objects.filter(id=item['client']).values('phone_number', 'first_name')
        for phone in all_phones:
            client = {
                'id': item['id'],
                'name': phone['first_name'],
                'phone_number': phone['phone_number'],
                'message': item['message'],
            }
            client_phones.append(client)
    return client_phones


@app.task
def send_messages_task(user: str, mailing_id: int) -> None:
    """Собираем сообщение в единое"""
    try:
        # Получаем объект рассылки
        mailing = MailingCommerceOffer.objects.select_related('city', 'company_detail').prefetch_related(
            'photo').get(id=mailing_id)
    except ObjectDoesNotExist:
        logger.error(f"MailingCommerceOffer с id={mailing_id} не найден")
        raise ValueError(f"MailingCommerceOffer с id={mailing_id} не найден")
    try:
        # Получаем объект шаблона
        template = TemplateForChannel.objects.get(name__icontains='предложение')
    except ObjectDoesNotExist:
        logger.error(f"TemplateForChannel does not exist")
        raise ValueError(f"TemplateForChannel с именем, содержащим 'предложение', не найден")
    # если указан город, то берём по нему, если нет, то всех
    clients = Client.objects.filter(city=mailing.city) if mailing.city else Client.objects.all()
    mailing_message = Template(template.templates_for_massage)
    company_detail = CompanyDetail.objects.get(name=mailing.company_detail)
    company_data = {
        'address': company_detail.address,
        'name': company_detail.name,
        'phone_number': company_detail.phone_number,
        'email': company_detail.email,
        'web_site': company_detail.web_site,
        'company_motto': company_detail.company_motto,
        'logo': company_detail.logo
    }
    commercial_offer = mailing_message.render(
        message=mailing.message,
        link=mailing.link,
        **company_data
    )
    # получаем все изображения
    image_data = list(item for item in mailing.photo.all()) if mailing.photo else []
    # перебираем информацию о компании для template
    # """Отправляем указанное коммерческое предложение"""
    try:
        loop = asyncio.get_event_loop()
        asyncio.set_event_loop(loop)
        task = loop.create_task(
            send_message_mailing(image_data=image_data, mailing_id=mailing_id, client_list=clients,
                                 commercial_offer=commercial_offer, admin_username='Razzakov_Timur', ))
        loop.run_until_complete(task)
    except Exception as e:
        # Логирование ошибки
        logger.error(f'data collected and sent to the bot: {str(e)}')


@app.task
def check_holiday_task():
    """Вызываем функцию, для проверки праздников сегодня и сохраняем в модель Result"""
    holiday()
    logger.info(f'data added')


@app.task
def check_birthday_task():
    """Вызываем функцию, для проверки дня рождения у клиентов и сохраняем в модель Result"""
    birthday()
    logger.info(f'data added')


@app.task
def send_congratulation_task():
    """Вызываем функцию, для проверки модели и рассылки по тг поздравлений"""
    try:
        loop = asyncio.get_event_loop()
        asyncio.set_event_loop(loop)
        task = loop.create_task(
            send_message_holiday(admin_username='Razzakov_Timur', client_data=get_data_from_result()))
        loop.run_until_complete(task)
        logger.info(f'data sent out')
    except Exception as e:
        # Логирование ошибки
        logger.error(f'send_congratulation_task: {str(e)}')


@app.task
def delete_old_task():
    """Удаляем старые данные, которым больше 5-дней. Чистим Result и MailingCommerceOffer"""
    Command.handle()
    logger.info(f'model checked and cleaned')
