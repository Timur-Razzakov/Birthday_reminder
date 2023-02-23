from django.urls import path

from .views import *

# app_name = 'scraping'
urlpatterns = [
    path('', show_all_client_birth_view, name='home'),
    path('add_mailing/', add_mailing_view, name='add_mailing'),
]



