from django.contrib import admin
from django.urls import path
from .views import NewUserView

app_name = 'registerapp'

urlpatterns = [
    path('', NewUserView.as_view(), name='newuserview'),

]
