from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from .forms import NewPropertyForm, PropertyImagesForm
from .models import PropertyImages, Property
from django.contrib import messages


def check_session(request, *args):

    #already_logged_in = function.is_seller
    flag = True
    for arg in args:
        flag = flag and request.session.get(arg, False)

    return flag


    # if not already_logged_in:
    #
    # else:
    #     #return CreateNewProperty.as_view()(request)
    #     return function.as_view()(request)


class CreateNewProperty(View):

    def get(self,request):
        if check_session(request,'logged_in','is_seller'):
            context={
                'property_form': NewPropertyForm(),
                'property_image': PropertyImagesForm()
            }
            return render(request, 'property_register.html', context=context)
        else:
            messages.add_message(request, messages.INFO, "Not Logged In, Please login as seller to post a property")
            return redirect('loginapp:check_login')

    def post(self):

        images_uploaded = self.request.FILES.getlist('Property_Images')
        form_data = NewPropertyForm(self.request.POST)
        if form_data.is_valid():
            property_form = form_data.save(commit=False)
            property_form.property_poster_id = self.request.user.id
            property_form.save()
            total_uploads = 5 if len(images_uploaded)>5 else len(images_uploaded)
            for i in range(total_uploads):
                PropertyImages.objects.create(property_image=images_uploaded[i], property_name_id=property_form.id)
            return HttpResponse('all set')
        else:
            return HttpResponse(form_data.errors)


class ExistingProperty(View,id):

    def get(self,request):
        if check_session(request,'logged_in'):
            is_buyer = not check_session(request, 'is_seller')
            if is_buyer:
                property = Property.objects.get(pk=id)
                context={'property':property}
                print(property)
                return render(request, 'property_view.html', context=context)
        else:
            messages.add_message(request, messages.INFO, "Not Logged In, Please login to view the property")
            return redirect('loginapp:check_login')
