from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_list_or_404
from django.views import View
from registerapp.models import NewUser
from propertyapp.models import Enquiry, Property, PropertyImages
from django.contrib import messages


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
            return render(request,'update_user_form.html', {'user': current_user})
        elif request.POST.get('update_profile'):
            current_user.first_name = request.POST.get('first_name')
            current_user.last_name = request.POST.get('last_name')
            current_user.description = request.POST.get('description')
            if request.FILES.get('profile_image'):
                current_user.profile_image = request.FILES.get('profile_image')
            current_user.save()
            return HttpResponse('User profile saved successfully')
