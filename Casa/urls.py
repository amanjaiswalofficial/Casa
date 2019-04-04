from django.contrib import admin
from django.urls import path, include
from registerapp.views import NewUserView
from loginapp.views import LoginFormView, check_login_function
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', include('registerapp.urls')),
    path('dashboard/', include('userdashboardapp.urls')),
    path('login/', include('loginapp.urls'), name='loginapp')
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
