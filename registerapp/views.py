from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from .forms import NewUserForm

class NewUserView(FormView):

    form_class = NewUserForm
    template_name = 'registerapp/userfields_form_2.html'#right now using form_2

    #All set for now
    def form_valid(self, form):
        form.save()
        #change to go somewhere else
        return redirect('propertyapp:showfeaturedpage')

    def form_invalid(self, form):
        """if invalid return error and back to it"""
        return render(self.request, self.template_name, {'form': form, 'error': form.errors})

    """in html, error is handled as
    {% for items in error.values %}
    {{items}}
    {% endfor %}
    """