from django.urls import path
from .views import ExistingProperty, CreateNewProperty, show_featured_page

app_name='propertyapp'
urlpatterns = [
    path('', CreateNewProperty.as_view(), name='propertyfeatured'),
    path('<int:id>/',ExistingProperty.as_view(), name='existingproperty'),
    path('featured/',show_featured_page, name='showfeaturedpage')

]