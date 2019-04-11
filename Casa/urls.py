from django.contrib import admin
from django.urls import path, include
from registerapp.views import NewUserRegistration
from loginapp.views import logout_user
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', include('registerapp.urls'), name='registerapp'),
    path('dashboard/', include('userdashboardapp.urls'), name='dashboardapp'),
    path('login/', include('loginapp.urls'), name='loginapp'),
    path('logout/', logout_user, name='logoutapp'),
    path('property/', include('propertyapp.urls'), name='propertyapp')
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
