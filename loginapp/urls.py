from django.urls import path
from .views import check_login_function

app_name = 'loginapp'


urlpatterns = [
    path('',check_login_function, name='check_login')
    ]