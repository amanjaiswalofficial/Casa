from django.urls import path
from .views import UserDashboardApp, UserQueryResponses

app_name = 'userdashboardapp'

urlpatterns = [
    path('', UserDashboardApp.as_view(), name='userdashboard'),
    path('responses/', UserQueryResponses.as_view(), name='userqueryresponse')

]