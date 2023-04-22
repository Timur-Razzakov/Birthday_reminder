from django.core.exceptions import ValidationError
from django.db import models
from PIL import Image

from accounts.models import Client, CompanyDetail, Channel, Gender, City
from reminder_service.custom_validators import TEMPLATE_NAME, validate_photo_size, MAX_PHOTOS, MAX_PHOTO_SIZE, \
    validate_video_extension


class TemplateForChannel(models.Model):
    """Модель для шаблона сообщений"""
    name = models.CharField(choices=TEMPLATE_NAME, max_length=255, verbose_name='template_name')
    channel = models.ForeignKey(Channel, verbose_name='channel', on_delete=models.CASCADE, null=True,
                                blank=True)
    templates_for_massage = models.TextField(verbose_name='templates_for_massage')
    gender = models.ForeignKey(Gender, verbose_name='GENDER', blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return "%s, %s " % (self.name, self.gender)


class Holiday(models.Model):
    """Модель для праздников и поздравлений"""
    image = models.ImageField(verbose_name='Изображение', upload_to='holiday/%Y/%m/%d',
                              blank=True, null=True, validators=[validate_photo_size])
    name = models.CharField(max_length=255, verbose_name='Holiday name')
    date = models.DateField(verbose_name='Holiday date', blank=True, null=True)
    congratulation = models.TextField(verbose_name='congratulate_text')
    gender = models.ForeignKey(Gender, verbose_name='GENDER', null=True,
                               blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.pk)


class MailingCommerceOffer(models.Model):
    """Модель для рассылки коммерческих предложений"""

    image = models.ManyToManyField('MultipleImage', blank=True, )
    video = models.ManyToManyField('MultipleVideo', blank=True, )
    message = models.TextField(verbose_name='message')
    link = models.URLField(max_length=255, unique=True, verbose_name='url',
                           null=True, blank=True)
    company_detail = models.ForeignKey(CompanyDetail, verbose_name='company_detail', on_delete=models.CASCADE,
                                       )
    created_at = models.DateTimeField(verbose_name="created_at", auto_now_add=True)
    city = models.ForeignKey(City, verbose_name='City', on_delete=models.CASCADE, null=True,
                             blank=True)
    sending_status = models.CharField(verbose_name='sending_status', max_length=90, null=True,
                                      blank=True, default=False)

    # функция, для вывода 1 изображения при использовании ManyToMany в шаблоне
    def get_first_image(self):
        return self.image.first().image.url if self.image.first() else None

    def __str__(self):
        return str(self.pk)


class MultipleImage(models.Model):
    image = models.ImageField(validators=[validate_photo_size], verbose_name=' Изображение',
                              upload_to='media/%Y/%m/%d', blank=True, null=True)

    def __str__(self):
        return str(self.image)


class MultipleVideo(models.Model):
    video = models.FileField(validators=[validate_video_extension], verbose_name=' Видео',
                             upload_to='video/', blank=True, null=True)

    def __str__(self):
        return str(self.video)


class Result(models.Model):
    """Модель для итоговых данных для поздравления клиентов"""

    client = models.ManyToManyField(Client, verbose_name="Client")
    process_date = models.DateTimeField(verbose_name='sent_to', null=True, blank=True)
    created_at = models.DateTimeField(verbose_name="created_at", null=True, blank=True, auto_now_add=True)  #
    channels = models.ForeignKey(Channel, on_delete=models.SET_NULL, verbose_name='channels for send',
                                 null=True, blank=True)
    image = models.ForeignKey(Holiday, on_delete=models.SET_NULL, verbose_name='image',
                              null=True, blank=True)
    message = models.TextField(verbose_name="Message")  #
    sending_status = models.CharField(verbose_name='sending_status', max_length=90, null=True,
                                      blank=True, default=False)

    def __str__(self):
        return str(self.sending_status)
