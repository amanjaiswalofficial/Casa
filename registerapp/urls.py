from django.contrib import admin
from django.urls import path
from .views import NewUserRegistration, buyerorseller

app_name = 'registerapp'

urlpatterns = [
    path('', buyerorseller, name='buyerorseller'),
    path('new/<str:users>',NewUserRegistration, name='newuserview')

]
