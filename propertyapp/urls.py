from django.urls import path
from .views import ExistingProperty, CreateNewProperty

urlpatterns = [
    path('', CreateNewProperty.as_view(), name='propertyfeatured'),
    path('<int:id>/',ExistingProperty.as_view(), name='existingproperty')

]