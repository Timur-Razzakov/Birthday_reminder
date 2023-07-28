# from django.test import TestCase, Client as cl_django
# from django.urls import reverse
#
# from tests.conftest import Setting, CreateAdmin
#
#
# class TestViews(Setting,CreateAdmin):
#     def setUp(self):
#         self.client = cl_django()
#
#     def check_view(self, url_name, html_name, text_for_check, item_id=None):
#         # Авторизуемся с помощью тестового клиента
#         self.client.force_login(self.user)
#         # Если item_id не равно None, то добавляем его к аргументам функции reverse()
#         if item_id is not None:
#             # Выполняем GET-запрос к URL
#             response = self.client.get(reverse(url_name, args=[item_id]))
#         else:
#             response = self.client.get(reverse(url_name))
#         content = response.content.decode('utf-8')
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, html_name)
#         self.assertContains(
#             response, text_for_check)
#
#     # reminder app
#     def test_show_all_client_view(self):
#         # show_all_client_view
#         self.check_view('home', 'home.html',
#                         'Сервис по рассылки коммерческих предложений')
#
#     def test_searchView(self):
#         # searchView
#         self.check_view('search', 'clients_list.html',
#                         'Клиентов с такими данными не найдены')
#
#     def test_show_all_clients_view(self):
#         # show_all_clients_view
#         self.check_view('show_clients', 'clients_list.html',
#                         'Результаты поиска согласно Вашему запросу')
#
#     def test_add_mailing_view(self):
#         # add_mailing_view
#         self.check_view('add_mailing', 'add_mailing.html',
#                         'Рассылка предложений')
#
#     def test_show_mailings_view(self):
#         # show_mailings_view
#         self.check_view('show_mailings', 'show_mailing.html',
#                         'Список всех коммерческих предложений')
#
#     # проверка, что тестовые данные  есть
#     def test_02_show_mailings_view(self):
#         # show_mailings_view
#         self.check_view('show_mailings', 'show_mailing.html',
#                         self.mailing_message)
#
#     def test_update_mailing_view(self):
#         # update_mailing_view
#         self.check_view('update_mailing', 'add_mailing.html',
#                         self.company_name, 1)
#
#     # ## --------------------------------------------------
#     # def test_send_mailing_view(self):
#     #     # send_mailing_view
#     #     self.check_view('send_mailing', 'show_mailings.html',
#     #                     'Успешно отправлено!!', 1)
#     # ## -----------------------------------------------------
#
#     def test_add_holiday_view(self):
#         # add_holiday_view
#         self.check_view('add_holiday', 'add_holiday.html',
#                         'Праздники')
#
#     def test_show_holiday_view(self):
#         # show_holiday_view
#         self.check_view('show_holiday', 'show_holiday.html',
#                         self.holiday_name)
#
#     def test_update_holiday_view(self):
#         # update_holiday_view
#         self.check_view('update_holiday', 'add_holiday.html',
#                         self.holiday_date, 1)
#     # --------------------------------------------------------------------
#     # account app
#
#     def test_login_view(self):
#         # login_view
#         self.check_view('login', 'accounts/login.html',
#                         'Форма входа' )
#
#     def test_add_client_view(self):
#         # add_client_view
#         self.check_view('add_client', 'accounts/add_client.html',
#                         'Новый клиент', )
#
#     def test_update_client_view(self):
#         # update_client_view
#         self.check_view('update_client', 'accounts/add_client.html',
#                         self.passport, 1)
#
#     def test_add_company_info_view(self):
#         # add_company_info_view
#         self.check_view('add_company', 'accounts/company_detail.html',
#                         'О Компании')
#
#     def test_show_all_company_view(self):
#         # show_all_company_view
#         self.check_view('show_company_detail', 'accounts/show_company_detail.html',
#                         self.email,)
#
#     def test_update_company_detail_view(self):
#         # update_company_detail_view
#         self.check_view('update_company_detail', 'accounts/company_detail.html',
#                         self.email, 1)
