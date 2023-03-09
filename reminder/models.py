from django.db import models

from accounts.models import Client, CompanyDetail, Channel, Gender, City


class TemplateForChannel(models.Model):
    """Модель для шаблона сообщений"""

    channel = models.ForeignKey(Channel, verbose_name='channel', on_delete=models.CASCADE, null=True,
                                blank=True)
    templates_for_massage = models.TextField(verbose_name='templates_for_massage')
    gender = models.ForeignKey(Gender, verbose_name='GENDER', on_delete=models.CASCADE)

    def __str__(self):
        return "%s, %s " % (self.channel, self.gender)


class Holiday(models.Model):
    """Модель для праздников и поздравлений"""
    image = models.ImageField(verbose_name=' images', upload_to='media/holiday//%Y/%m/%d',
                              blank=True)
    name = models.CharField(max_length=255, verbose_name='Holiday name')
    date = models.DateField(verbose_name='Holiday date')
    congratulation = models.TextField(verbose_name='congratulate_text')

    def __str__(self):
        return "%s, %s " % (self.name, self.date)


class MailingCommerceOffer(models.Model):
    """Модель для рассылки коммерческих предложений"""

    photo = models.ImageField(verbose_name=' images', upload_to='media/%Y/%m/%d', blank=True)
    message = models.TextField(verbose_name='message')
    link = models.URLField(max_length=255, unique=True, verbose_name='url',
                           null=True, blank=True)
    company_detail = models.ForeignKey(CompanyDetail, verbose_name='company_detail', on_delete=models.CASCADE,
                                       )
    sending_status = models.CharField(verbose_name='sending_status', max_length=90, null=True,
                                      blank=True, default=False)
    created_at = models.DateTimeField(verbose_name="created_at", auto_now_add=True)
    city = models.ForeignKey(City, verbose_name='City', on_delete=models.CASCADE, null=True,
                             blank=True)

    def __str__(self):
        return "%i, %s " % (self.pk, self.sending_status)


class Result(models.Model):
    """Модель для итоговых данных для отправки и рассылки клиентам"""

    client = models.ManyToManyField(Client, verbose_name="Client")
    process_date = models.DateTimeField(verbose_name='sent_to', null=True, blank=True)
    created_at = models.DateTimeField(verbose_name="created_at", null=True, blank=True, auto_now_add=True)  #
    channels = models.ForeignKey(Channel, on_delete=models.SET_NULL, verbose_name='channels for send',
                                 null=True, blank=True)
    message = models.TextField(verbose_name="Message")  #
    sending_status = models.CharField(verbose_name='sending_status', max_length=90, null=True,
                                      blank=True, default=False)  # --

    def __str__(self):
        return str(self.sending_status)
