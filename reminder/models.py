from django.core.validators import RegexValidator, URLValidator
from django.db import models
from accounts.models import Client, CompanyDetail, Channel

from reminder_service.custom_validators import GENDER, HOLIDAY


class TemplateForChannel(models.Model):
    """Модель для шаблона сообщений"""

    channel = models.ForeignKey(Channel, verbose_name='channel', on_delete=models.CASCADE, null=True,
                                blank=True)
    templates_for_massage = models.TextField(verbose_name='templates_for_massage')
    gender = models.CharField(choices=GENDER, verbose_name='GENDER', max_length=9)

    def __str__(self):
        return "%s, %s " % (self.channel, self.gender)


class Holiday(models.Model):
    """Модель для праздников и поздравлений"""

    name = models.CharField(choices=HOLIDAY, max_length=100, verbose_name='Holiday name')
    date = models.DateField(verbose_name='Holiday date', null=True, blank=True)
    congratulation = models.TextField(verbose_name='congratulation', blank=True, null=True)

    def __str__(self):
        return "%s, %s " % (self.name, self.date)


class MailingCommerceOffer(models.Model):
    """Модель для рассылки коммерческих предложений"""

    photo = models.ImageField(verbose_name=' images', upload_to='media/%Y/%m/%d', blank=True)
    message = models.TextField(verbose_name='message', blank=True, null=True)
    link = models.URLField(max_length=255, unique=True, verbose_name='url',
                           null=True, blank=True)
    company_detail = models.ForeignKey(CompanyDetail, verbose_name='company_detail', on_delete=models.CASCADE,
                                       null=True,
                                       blank=True)
    sending_status = models.CharField(verbose_name='sending_status', max_length=90, null=True,
                                      blank=True, default=False)
    created_at = models.DateTimeField(verbose_name="created_at", auto_now_add=True)

    def __str__(self):
        return "%i, %s " % (self.pk, self.sending_status)


# class CongratulateClient(models.Model):
#     """Модель для поздравления клиентов с днём рождения"""
#
#     client_name = models.ForeignKey(Client, verbose_name='client_name', on_delete=models.CASCADE, null=True,
#                                     blank=True)
#     message = models.TextField(verbose_name='templates_for_massage')
#     created_at = models.DateTimeField(verbose_name="created_at", auto_now_add=True)
#
#     def __str__(self):
#         return "%i, %s " % (self.pk, self.created_at)


class Result(models.Model):
    """Модель для итоговых данных для отправки и рассылки клиентам"""

    client = models.ManyToManyField(Client, verbose_name="Client")#

    process_date = models.DateTimeField(verbose_name='sent_to', null=True, blank=True)
    created_at = models.DateTimeField(verbose_name="created_at", null=True, blank=True, auto_now_add=True)#
    channels = models.ForeignKey(Channel, on_delete=models.SET_NULL, verbose_name='channels for send',
                                 null=True, blank=True)
    message = models.TextField(verbose_name="Message")#
    sending_status = models.CharField(verbose_name='sending_status', max_length=90, null=True,
                                      blank=True, default=False)  # --

    def __str__(self):
        return str(self.sending_status)
