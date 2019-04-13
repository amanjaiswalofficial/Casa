from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_list_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import UpdateView
from registerapp.forms import NewUserForm
from registerapp.models import NewUser
from propertyapp.models import Enquiry, Property, PropertyImages
from django.contrib import messages
from .forms import NewUserUpdateForm


class UserDashboardApp(View):

    def get(self,request):
        return self.show_user()

    def show_user(self):
        username = self.request.session.get('current_user')
        is_seller = self.request.session.get('is_seller', False)
        try:
            current_user = NewUser.objects.get(username=username)
            context = {'user': current_user}
            if is_seller:
                return self.show_seller(current_user, context)
            else:
                return self.show_buyer(current_user, context)
        except NewUser.DoesNotExist:
            messages.add_message(self.request, messages.INFO, "Login in first to view dashboard")
            return redirect('loginapp:check_login')

    def show_seller(self, current_user, context):
        queries_for_seller=[]
        try:
            posted_properties_images = []
            posted_properties = list(Property.objects.filter(property_poster_id=current_user.id))

            for property in posted_properties:
                posted_properties_images.append(PropertyImages.objects.filter(property_name_id=property.id)[0])
            final_property = zip(posted_properties, posted_properties_images)
            queries_for_seller = get_list_or_404(Enquiry, property__property_poster=current_user)
        except Property.DoesNotExist:
            posted_properties = False
            posted_properties_images = False
            final_property = False
        except Enquiry.DoesNotExist:
            queries_for_seller = False
        finally:
            context['queries_for_seller'] = queries_for_seller
            context['posted_properties'] = posted_properties
            context['posted_properties_image'] = posted_properties_images
            context['final_properties'] = final_property
            return render(self.request, 'dashboard_seller.html', context=context)

    def show_buyer(self, current_user, context):
        queries_made=[]
        try:
            queries_made = get_list_or_404(Enquiry, enquiry_user=current_user)
        except Http404:
            queries_made = False
        finally:
            context['queries_made'] = queries_made
            return render(self.request, 'dashboard_buyer.html', context=context)

    def post(self, request):
        username = self.request.session.get('current_user')
        current_user = NewUser.objects.get(username=username)
        if request.POST.get('update_profile_button'):
            return UpdateUser.as_view()(request, pk=current_user.id)
        elif request.POST.get('update_profile'):
            # current_user.first_name = request.POST.get('first_name')
            # current_user.last_name = request.POST.get('last_name')
            # current_user.description = request.POST.get('description')
            # if request.FILES.get('profile_image'):
            #     current_user.profile_image = request.FILES.get('profile_image')
            # current_user.save()
            # return HttpResponse('User profile saved successfully')
            return UpdateUser.as_view()(request, pk=current_user.id)

class UpdateUser(UpdateView):
        model = NewUser
        form_class = NewUserUpdateForm
        template_name = 'update_user.html'

        def get(self, request, *args, **kwargs):
            """
            Method to handle and decide whether allowing the logged in user to update the property or not
            :return: Either the form containing values to update the properties or login page to login as seller
            """

            if self.request.session.get('logged_in', False):
                    print(self.current_user.is_seller)
                    return super().get(request, *args, **kwargs)
            else:
                    messages.add_message(self.request, messages.INFO, "Please login as seller to post a property")
                    return redirect('loginapp:check_login')

        def get_context_data(self, **kwargs):
            context = super(UpdateUser, self).get_context_data(**kwargs)
            username = self.request.session.get('current_user')
            current_user = NewUser.objects.get(username=username)
            #print(current_user.description)
            context['current_user'] = current_user
            return context

        def form_valid(self, form):
            context = self.get_context_data()
            form.instance.is_seller = context['current_user'].is_seller
            form.instance.save()
            return redirect('userdashboardapp:userdashboard')


        # def form_valid(self, form):
        #     import pdb;
        #     pdb.set_trace()
        #
        # def form_invalid(self, form, **kwargs):
        #     print('inside invalid')
        #     import pdb;
        #     pdb.set_trace()
        #     context=self.get_context_data()
        #     return render(self.request, self.template_name,context=context)

