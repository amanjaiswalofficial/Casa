from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.hashers import make_password
# Create your views here.
from .models import User, NewUser
from django.views.generic.edit import CreateView
# Register your models here.

def successpage(request):
    return HttpResponse('Success')

class NewUserView(CreateView):

    model = NewUser
    template_name = 'registerapp/userfields_form.html'
    fields = ['username', 'email_field', 'password', 'first_name', 'last_name', 'description', 'profile_image', 'is_seller']
    #fields = ['username','email_field','password','profile_image']
    def form_valid(self, form):


        #return HttpResponse('All Good')

        password_valid = True if (len(form.data['password'])>=8) else False
        if password_valid:
            NewUserData = NewUser()
            for keys in self.fields:
                setattr(NewUserData, keys, form.cleaned_data[keys])
            NewUserData.password = make_password(form.cleaned_data['password'])
            NewUserData.is_staff = True
            NewUserData.is_superuser = True
            NewUserData.save()
            return reverse_lazy('success')
        else:
            return HttpResponse('Some error')
            #render(request, 'userfields_form.html', {password_error:'Invalid password, atleast 8 characters must be present'})
