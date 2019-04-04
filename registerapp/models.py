from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

username_pattern = '^[A-Za-z][\d\w.]{8,16}'
valid_name_pattern = '[A-Za-z\s]'
password_pattern = '(&|\^|%|$|#|@|\d|\w|!){8,16}'


class NewUser(User):
    user = models.OneToOneField(User, on_delete=models.CASCADE, parent_link=True)
    email_field = models.EmailField(max_length=30,
                                    unique=True,
                                    blank=False)
    description = models.TextField()
    profile_image = models.ImageField(upload_to='user_images/', default='register_app/blank_face.png')
    is_seller = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('success')
