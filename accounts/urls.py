from django.urls import path

from .views import *

# app_name = 'accounts'
urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    path('add_client/', add_client_view, name='add_client'),
    path('update_client/<int:id>/', update_client_view, name='update_client'),


    path('add_company/', add_company_info_view, name='add_company'),
    path('show_company_detail/', show_all_company_view, name='show_company_detail'),
    path('update_company/<int:id>/', update_company_detail_view, name='update_company_detail'),

]
