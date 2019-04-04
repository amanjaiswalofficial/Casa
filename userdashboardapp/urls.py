from django.urls import path
from .views import UserDashboardApp

urlpatterns = [
    path('', UserDashboardApp.as_view(), name='userdashboard'),

]