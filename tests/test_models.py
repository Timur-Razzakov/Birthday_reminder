from django.test import TestCase
from reminder.models import Result
from accounts.models import *
from tests.conftest import Setting, CreateAdmin


class TestModels(Setting, CreateAdmin):
    def test_Gender(self):
        # Тестирование поля name
        self.assertEqual(self.gender.name, self.gender_name)

    def test_City(self):
        # Тестирование поля name
        self.assertEqual(self.city.name, self.city_name)

    def test_Channel(self):
        # Тестирование поля name
        self.assertEqual(self.channel.name, self.channel_name)

    def test_CompanyDetail(self):
        # Тестирование поля name
        self.assertEqual(self.company_detail.name, self.company_name)
        self.assertEqual(self.company_detail.address, self.address)
        self.assertEqual(self.company_detail.phone_number, self.phone_number)
        self.assertEqual(self.company_detail.email, self.email)
        self.assertEqual(self.company_detail.web_site, self.url)
        self.assertEqual(self.company_detail.company_motto, self.company_motto)

    def test_Client(self):
        # Тестирование поля name
        self.assertEqual(self.client_comp.first_name, self.name)
        self.assertEqual(self.client_comp.last_name, self.last_name)
        self.assertEqual(self.client_comp.father_name, self.father_name)
        self.assertEqual(self.client_comp.email, self.email)
        self.assertEqual(self.client_comp.phone_number, self.phone_number)
        self.assertEqual(self.client_comp.inter_passport, self.inter_passport)
        self.assertEqual(self.client_comp.date_of_birth, self.date_of_birth)
        self.assertEqual(self.client_comp.passport, self.passport)
        self.assertEqual(str(self.client_comp.gender), self.gender_name)
        self.assertEqual(self.client_comp.address, self.address)
        self.assertEqual(str(self.client_comp.city), self.city_name)
        self.assertEqual(str(self.client_comp.channel), self.channel_name)
        self.assertEqual(self.client_comp.traveled, self.traveled)

    def test_MyUser(self):
        # Тестирование поля name
        self.assertEqual(self.user.email, self.admin_email)
        self.assertEqual(self.user.user_name, self.user_name)

    # reminder app

    def test_TemplateForChannel(self):
        # Тестирование поля name
        self.assertEqual(self.tempalete.name, self.templates_name)
        self.assertEqual(self.tempalete.templates_for_massage, self.templates_for_massage)
        self.assertEqual(str(self.tempalete.channel), self.channel_name)
        self.assertEqual(str(self.tempalete.gender), self.gender_name)

    def test_Holiday(self):
        # Тестирование поля name
        self.assertEqual(self.holiday.name, self.holiday_name)
        self.assertEqual(self.holiday.date, self.holiday_date)
        self.assertEqual(self.holiday.congratulation, self.holiday_message)
        self.assertEqual(str(self.holiday.gender), self.gender_name)

    def test_MailingCommerceOffer(self):
        # Тестирование поля name
        self.assertEqual(self.mailing.message, self.mailing_message)
        self.assertEqual(str(self.mailing.city), self.city_name)
        self.assertEqual(str(self.mailing.company_detail), self.company_name)

