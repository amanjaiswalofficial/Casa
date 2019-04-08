from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from .forms import NewPropertyForm, PropertyImagesForm
from .models import PropertyImages, Property
from django.contrib import messages
from django.views.generic.edit import UpdateView


def check_session(request, *args):

    flag = True
    for arg in args:
        flag = flag and request.session.get(arg, False)
    return flag


class CreateNewProperty(View):

    def get(self,request):
        if check_session(request,'logged_in','is_seller'):
            context={
                'property_form': NewPropertyForm(),
                'property_image': PropertyImagesForm()
            }
            return render(request, 'property_register.html', context=context)
        elif check_session(request,'logged_in'):
            messages.add_message(request, messages.INFO, "Not Logged In as Buyer, Please login as seller to post a property")
        else:
            messages.add_message(request, messages.INFO, "Not Logged In, Please login as seller to post a property")
        return redirect('loginapp:check_login')

    def post(self,request):

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


class ExistingProperty(View):

    def get(self,request,id):
        property = Property.objects.get(pk=id)
        property_images = PropertyImages.objects.filter(property_name_id=property.id)
        no_of_images = len(property_images)
        current_user = request.session.get('current_user')
        property_poster = property.property_poster
        context = {'property': property, 'property_images': property_images, 'no_of_images': range(no_of_images)}
        if check_session(request,'logged_in'):
            is_buyer = not check_session(request, 'is_seller')
            #NEED TO SET WHEN ENQUIRY MADE AS WELL
            if is_buyer:
                return render(request, 'property_view.html', context=context)
            elif current_user == str(property_poster):
                return render(request, 'property_update.html', context=context)
            return render(request, 'property_view.html', context=context)
        return render(request, 'property_view.html', context=context)
            #messages.add_message(request, messages.INFO, "Not Logged In, Please login to view the property")
            #return redirect('loginapp:check_login')

    def post(self,request,id):
        images_uploaded = self.request.FILES.getlist('property_images')
        form_data = NewPropertyForm(self.request.POST)
        if form_data.is_valid():
            current_property = Property.objects.get(pk=id)
            property_form = form_data.save(commit=False)
            property_form.property_poster_id = self.request.user.id
            string_fields = ['property_title',
                             'property_address',
                             'property_description']
            int_fields = ['property_pin',
                          'property_price',
                          'property_bedroom',
                          'property_bathroom',
                          'property_sq_feet',
                          'property_lot_size',
                          'property_garage',
                          ]
            for field in string_fields:
                setattr(current_property,field,self.request.POST.get(field))
            for field in int_fields:
                setattr(current_property,field,int(self.request.POST.get(field)))
            current_property.save()
            print(current_property.id)
            PropertyImages.objects.filter(property_name_id=current_property.id).delete()
            total_uploads = 5 if len(images_uploaded) > 5 else len(images_uploaded)
            for i in range(total_uploads):
                PropertyImages.objects.create(property_image=images_uploaded[i], property_name_id=current_property.id)
            return HttpResponse('all set')
        else:
            return HttpResponse(form_data.errors)


class GetEnquiry(View):

    def get(self):
        pass

    def post(self):
        pass