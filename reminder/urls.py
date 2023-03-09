from django.urls import path

from .views import *

# app_name = 'scraping'
urlpatterns = [
    path('', show_all_client_view, name='home'),
    path('add_mailing/', add_mailing_view, name='add_mailing'),
    path('add_holiday/', add_holiday_view, name='add_holiday'),
    # path('search/', views.SearchView.as_view(), name='search'),
    path('search/', searchView, name='search'),
]



