import re

from django.contrib.auth.forms import UserCreationForm

from registerapp.models import NewUser

class NewUserUpdateForm(UserCreationForm):

    class Meta:
        model = NewUser
        fields = ['first_name', 'password1',
                  'last_name', 'description', 'phone_number',
                  'profile_image', 'is_seller']

    def clean(self):
        cd = self.cleaned_data
        usernames=[]
        useremail=[]
        current_users = NewUser.objects.all()
        for user in current_users:
            usernames.append(user.username)
            useremail.append(user.email_field)
        patter_number = re.compile("^(?:(?:\+|0{0,2})91(\s*[\ -]\s*)?|[0]?)?[789]\d{9}|(\d[ -]?){10}\d$")

        if not re.match(patter_number, str(cd.get("phone_number"))):
            self.add_error('phone_number', "The phone number must be in Indian Format +91 starting or with "
                                    "977587666,0 9754845789,0-9778545896,+91 9456211568,91 9857842356,"
                                    "919578965389,03595-259506,03592 245902")

        return cd