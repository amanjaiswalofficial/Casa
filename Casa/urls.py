from django.contrib import admin
from django.urls import path, include
from loginapp.views import logout_user
from django.conf.urls.static import static
from django.conf import settings
from propertyapp.views import show_featured_page, handle_error
urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', include('registerapp.urls'), name='registerapp'),
    path('dashboard/', include('userdashboardapp.urls'), name='dashboardapp'),
    path('login/', include('loginapp.urls'), name='loginapp'),
    path('logout/', logout_user, name='logoutapp'),
    path('property/', include('propertyapp.urls'), name='propertyapp'),
    path('',show_featured_page)
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404=handle_error
handler500=handle_error