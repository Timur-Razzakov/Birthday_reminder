import shutil
import tempfile

from django.conf import settings
from django.test import TestCase

from accounts.models import City, Channel, Gender, Client, CompanyDetail, MyUser
from reminder.models import Holiday, TemplateForChannel, MailingCommerceOffer



class CreateAdmin(TestCase):
    """Создаём админа"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.admin_email = 'admin@gmail.com'
        cls.admin_password = 'admin'
        cls.user_name = '@Razzakov_Timur'
        # создаём админа
        cls.user = MyUser.objects.create_user(email=cls.admin_email, password=cls.admin_password,
                                              user_name=cls.user_name)


class Setting(TestCase):
    """Создание данных для тестирования"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создаём временную папку для изображений
        settings.MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)

        cls.email = 'razz330@gmail.com'
        cls.email_02 = 'zadr99933@gmail.co'
        cls.address = 'Uzbekistan 42A'
        cls.company_name = 'TrevelTR'
        cls.company_name_02 = 'TrevelRT'
        cls.holiday_name = 'New year'
        cls.city_name = 'Фергана'
        cls.gender_name = 'Мужчина'
        cls.name = 'Тимур'
        cls.channel_name = 'Телеграмм'
        cls.last_name = 'Раззаков'
        cls.father_name = 'Алишерович'
        cls.phone_number = '+998999951509'
        cls.date_of_birth = '1998-09-15'
        cls.inter_passport = 'AA7999474'
        cls.passport = 'AA7999479'
        cls.traveled = 'Самарканд'
        cls.url = 'http://138.2.173.149/accounts/'
        cls.company_motto = 'Всегда вместе!!'
        cls.mailing_message = 'hello Django'
        cls.holiday_message = 'congratulation!!'
        cls.holiday_date = '2023-07-29'
        cls.templates_for_massage = '{{message}}'
        cls.templates_name = 'Праздники'

        cls.city = City.objects.create(name=cls.city_name)
        cls.gender = Gender.objects.create(name=cls.gender_name)
        cls.channel = Channel.objects.create(name=cls.channel_name)
        # Создаём клиента
        cls.client_comp = Client.objects.create(
            first_name=cls.name,
            last_name=cls.last_name,
            father_name=cls.father_name,
            email=cls.email,
            phone_number=cls.phone_number,
            date_of_birth=cls.date_of_birth,
            inter_passport=cls.inter_passport,
            passport=cls.passport,
            gender=cls.gender,
            address=cls.address,
            city=cls.city,
            channel=cls.channel,
            traveled=cls.traveled
        )
        cls.company_detail = CompanyDetail.objects.create(
            name=cls.company_name,
            address=cls.address,
            web_site=cls.url,
            email=cls.email,
            phone_number=cls.phone_number,
            company_motto=cls.company_motto,
            logo=tempfile.NamedTemporaryFile(suffix='.jpg').name,
        )
        cls.holiday = Holiday.objects.create(
            name=cls.holiday_name,
            date=cls.holiday_date,
            congratulation=cls.holiday_message,
            gender=cls.gender,
            image=tempfile.NamedTemporaryFile(suffix='.jpg').name,
        )
        cls.tempalete = TemplateForChannel.objects.create(
            name=cls.templates_name,
            templates_for_massage=cls.templates_for_massage,
            channel=cls.channel,
            gender=cls.gender,
        )

        cls.mailing = MailingCommerceOffer.objects.create(
            message=cls.mailing_message,
            city=cls.city,
            company_detail=cls.company_detail,
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        # Удаляем временную папку после завершения тестов
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)
