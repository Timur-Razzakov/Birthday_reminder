from django.urls import path

from .views import *

# app_name = 'accounts'
urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    # path('delete/', delete_view, name='delete_user'),
    # path('registration/', register_view, name='registration'),
    # path('get_clients/', show_all_client_birth_view, name='get_clients'),
    path('add_client/', add_client_birth_view, name='add_client'),
    path('add_company/', add_company_info_view, name='add_company'),
]
