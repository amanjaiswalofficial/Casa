from django.contrib import admin
from django.urls import path
from registerapp.views import NewUserView
from loginapp.views import LoginFormView, check_login_function

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', NewUserView.as_view(), name='register'),
    #path('login/', LoginFormView.as_view(), name='login')
    path('login/', check_login_function, name = 'login')
]
