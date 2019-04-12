from django.urls import path
from .views import ExistingProperty, CreateNewProperty, show_featured_page, DeleteProperty, search_property, show_home_page, UpdateProperty

app_name='propertyapp'
urlpatterns = [
    path('', CreateNewProperty.as_view(), name='propertyfeatured'),
    path('<int:id>/', ExistingProperty.as_view(), name='existingproperty'),
    path('featured/', show_featured_page, name='showfeaturedpage'),
    path('homepage/',show_home_page, name='showhomepage'),
    path('delete/<int:pk>', DeleteProperty.as_view(), name='deleteproperty'),
    path('search', search_property, name='searchproperty'),
    path('update/<int:pk>', UpdateProperty.as_view(), name='updateproperty')
]