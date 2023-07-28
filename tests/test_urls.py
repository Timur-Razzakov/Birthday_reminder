# from http import HTTPStatus
#
# from django.test import TestCase, Client
# from django.urls import reverse, resolve
# from django.contrib.auth.models import User
#
# from accounts import urls
# from accounts.models import MyUser, MyUserManager
# from tests.conftest import Setting, CreateAdmin
#
#
# class UrlTest(Setting,CreateAdmin):
#     def setUp(self):
#         self.client = Client()
#
#     def test_urls(self):
#         # Авторизуемся с помощью тестового клиента
#         self.client.force_login(self.user)
#         # Создаем список URL-адресов, которые вы хотите проверить
#         urls_to_check = {
#             # accounts
#             'login': 'login_view',
#             'add_client': 'add_client_view',
#             'add_company': 'add_company_info_view',
#             # reminder
#             'home': 'show_all_client_view',
#             'show_mailings': 'show_mailings_view',
#             'add_holiday': 'add_holiday_view',
#             'show_holiday': 'show_holiday_view',
#             'search': 'searchView',
#             'show_clients': 'show_all_clients_view',
#             'add_mailing': 'add_mailing_view',
#             'show_company_detail': 'show_all_company_view',
#         }
#
#         for url, view in urls_to_check.items():
#             # Получаем URL для представления login_view
#             get_url = reverse(url)
#             # Выполняем GET-запрос к URL
#             response = self.client.get(get_url)
#             print(f"Testing URL: {url}, View: {view}")
#             self.assertEqual(response.status_code, HTTPStatus.OK)
#             # Проверяем, что используется правильное представление (view)
#             self.assertEqual(response.resolver_match.func.__name__, view)
#
#         # url, где нужно получать подробную информацию о товаре
#         url_for_show_detail = {
#             # accounts
#             'update_company_detail': 'update_company_detail_view',
#             'update_client': 'update_client_view',
#             # reminder
#             'update_holiday': 'update_holiday_view',
#             'update_mailing': 'update_mailing_view',
#             # 'send_mailing': 'send_mailing_view',
#         }
#         for url, view in url_for_show_detail.items():
#             # Получаем URL для представления login_view
#             get_url = reverse(url, args=[1])
#             # Выполняем GET-запрос к URL
#             response = self.client.get(get_url)
#             print(f"Testing URL: {url}, View: {view}")
#             self.assertEqual(response.status_code, HTTPStatus.OK)
#             # Проверяем, что используется правильное представление (view)
#             self.assertEqual(response.resolver_match.func.__name__, view)
