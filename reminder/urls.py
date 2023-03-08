from django.urls import path

from .views import *

# app_name = 'scraping'
urlpatterns = [
    path('', show_all_client_view, name='home'),
    path('add_mailing/', add_mailing_view, name='add_mailing'),
    # path('search/', views.SearchView.as_view(), name='search'),
    path('clients_list/', searchView, name='clients_list'),
]



