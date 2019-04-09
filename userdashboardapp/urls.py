from django.urls import path
from .views import UserDashboardApp

app_name = 'userdashboardapp'

urlpatterns = [
    path('', UserDashboardApp.as_view(), name='userdashboard'),

]