# from django.test import TestCase, Client
# from django.core import mail
# from reminder import forms as reminder_forms
# from accounts import forms as accounts_form
# from tests.conftest import CreateAdmin, Setting
#
#
# class TestForm(Setting, CreateAdmin):
#     """Тест Форм"""
#
#     def setUp(self):
#         self.client = Client()
#
#     def test_UserLoginForm(self):
#         form = accounts_form.UserLoginForm({
#             'email': self.admin_email,
#             'password': self.admin_password
#         })
#         self.assertTrue(form.is_valid())
#
#     def test_CityFrom(self):
#         form = accounts_form.CityFrom({
#             'name': self.city_name
#         })
#         self.assertTrue(form.is_valid())
#
#     def test_ClientForm(self):
#         form = accounts_form.ClientForm({
#             'first_name': self.name,
#             'last_name': self.last_name,
#             'father_name': self.father_name,
#             'email': self.email_02,
#             'phone_number': self.phone_number,
#             'date_of_birth': self.date_of_birth,
#             'inter_passport': self.inter_passport,
#             'passport': self.passport,
#             'gender': self.gender,
#             'address': self.address,
#             'city': self.city,
#             'channel': self.channel,
#             'traveled': self.traveled})
#         self.assertTrue(form.is_valid())
#
#     def test_CompanyDetailForm(self):
#         form = accounts_form.CompanyDetailForm({
#             'name': self.company_name_02,
#             'email': self.email_02,
#             'phone_number': self.phone_number,
#             'address': self.address,
#             'web_site': self.url,
#             'company_motto': self.company_motto
#         })
#
#         self.assertTrue(form.is_valid())
#
#     def test_SearchClientForm(self):
#         form = accounts_form.SearchClientForm({
#             'date_of_birth': self.date_of_birth,
#             'email': self.email_02,
#             'city': self.city,
#             'phone_number': self.phone_number
#         })
#
#         self.assertTrue(form.is_valid())
#
#     # reminder app
#     def test_HolidayFrom(self):
#         form = reminder_forms.HolidayFrom({
#             'name': self.holiday_name,
#             'date': self.holiday_date,
#             'gender': self.gender,
#             'congratulation': self.holiday_message,
#         })
#
#         self.assertTrue(form.is_valid())
#
#     def test_MailingCommerceOfferFrom(self):
#         form = reminder_forms.MailingCommerceOfferFrom({
#             'link': self.url,
#             'company_detail': self.company_detail,
#             'city': self.city,
#             'message': self.mailing_message,
#         })
#
#         self.assertTrue(form.is_valid())
