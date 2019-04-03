from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import FormView
from .forms import LoginForm
from django.contrib.auth import authenticate, logout, login
from registerapp.models import NewUser


class LoginFormView(FormView):

    form_class = LoginForm
    template_name = 'loginapp/login_page.html'

    """def post(self, request, *args, **kwargs):
        form = LoginForm(self.request.POST)
        import pdb;
        pdb.set_trace()
        """

    def form_valid(self, form):

        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        current_user = authenticate(request=self.request, username=username, password=password)
        if current_user is not None:
            login(self.request, current_user)
            self.request.session['logged_in'] = True
            self.request.session['current_user'] = username
            self.request.session['is_seller'] = NewUser.objects.get(username=username).is_seller
            import pdb;
            pdb.set_trace()
            return HttpResponse('All set')
        else:
            #FIX
            return HttpResponse('invalid user')

#CHANGE LOGGED IN VALUE TO FALSE ON LOGOUT

def check_login_function(request):

    already_logged_in = request.session.get('logged_in', False)
    if not already_logged_in:
        return LoginFormView.as_view()(request)
    else:
        #FIX
        return HttpResponse('already logged in brother!')

