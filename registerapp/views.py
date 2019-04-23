from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from .forms import NewUserForm


class NewUserRegistration(FormView):
    """Class to display form for user registration"""

    form_class = NewUserForm
    template_name = 'registerapp/registration_form.html'

    def form_valid(self, form):
        form.instance.is_seller = self.request.session.get('is_user_seller')
        form.save()
        return redirect('propertyapp:showfeaturedpage')

    def form_invalid(self, form):
        return render(self.request, self.template_name, {'form': form, 'error': form.errors})


def buyerorseller(request):
    """Method to set whether the user registering is a seller or a buyer"""

    if request.method == 'GET':
        return render(request, 'registerapp/buyer_or_seller.html')

    if request.method == 'POST':
        if request.POST.get('buyer_action') == "":
            request.session['is_user_seller'] = False
        elif request.POST.get('seller_action') == "":
            request.session['is_user_seller'] = True
        return NewUserRegistration.as_view()(request)




