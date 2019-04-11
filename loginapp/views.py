from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import FormView
from .forms import LoginForm
from django.contrib.auth import authenticate, logout, login
from registerapp.models import NewUser
from django.contrib import messages

class LoginFormView(FormView):

    form_class = LoginForm
    template_name = 'loginapp/login_page.html'

    def form_valid(self, form):

        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        current_user = authenticate(request=self.request, username=username, password=password)
        if current_user is not None:
            login(self.request, current_user)
            self.request.session['logged_in'] = True
            self.request.session['current_user'] = username
            self.request.session['is_seller'] = NewUser.objects.get(username=username).is_seller
            self.request.session['user_first_name'] = User.objects.get(username=username).first_name
            return redirect('propertyapp:showfeaturedpage')
        else:
            messages.add_message(self.request, messages.INFO, "Invalid username/password")
            return redirect('loginapp:check_login')


def check_user_login(request):

    already_logged_in = request.session.get('logged_in', False)
    if not already_logged_in:
        return LoginFormView.as_view()(request)
    else:
        #FIX GO TO HOME
        return HttpResponse('already logged in brother!')


def logout_user(request):

    if request.session.get('logged_in', False):
        logout(request)
        return redirect('propertyapp:showfeaturedpage')
    else:
        return HttpResponse('No user is currently logged in')