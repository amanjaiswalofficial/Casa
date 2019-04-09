from django.urls import path
from .views import check_user_login

app_name = 'loginapp'


urlpatterns = [
    path('',check_user_login, name='check_login')
    ]