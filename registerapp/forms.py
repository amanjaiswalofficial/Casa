from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import NewUser

class NewUserForm(UserCreationForm):

    class Meta:
        model = NewUser
        fields = ['username', 'email_field', 'first_name','password1', 'last_name', 'description', 'profile_image', 'is_seller']
