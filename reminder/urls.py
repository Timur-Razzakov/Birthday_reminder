from django.urls import path

from .views import *

# app_name = 'scraping'
urlpatterns = [
    path('', show_all_client_view, name='home'),
    path('search/', searchView, name='search'),
    path('show_clients/', show_all_clients_view, name='show_clients'),


    path('add_mailing/', add_mailing_view, name='add_mailing'),
    path('show_mailings/', show_mailings_view, name='show_mailings'),
    path('update_mailing/<int:id>/', update_mailing_view, name='update_mailing'),
    path('send_mailing/<int:id>/', send_mailing_view, name='send_mailing'),

    path('add_holiday/', add_holiday_view, name='add_holiday'),
    path('show_holiday/', show_holiday_view, name='show_holiday'),
    path('update_holiday/<int:id>/', update_holiday_view, name='update_holiday'),
]
