from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DeleteView
from registerapp.models import NewUser
from .forms import NewPropertyForm, PropertyImagesForm
from .models import PropertyImages, Property, Enquiry
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

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


def check_session(request, *args):

    flag = True
    for arg in args:
        flag = flag and request.session.get(arg, False)
    return flag


def show_property_for_buyer(request,context, current_user, current_property):
    context['is_not_seller'] = True
    current_user = User.objects.get(username=current_user)
    try:
        Enquiry.objects.get(property=current_property, enquiry_user=current_user)
        #return render(request, 'property_view.html', context=context)
        return render(request, 'property_details.html', context=context)
    except Enquiry.DoesNotExist:
        context['no_query_made'] = True
        return render(request, 'property_details.html', context=context)


def show_property_for_seller(request, context, current_user, property_poster):
    if current_user == str(property_poster):
        return render(request, 'property_details.html', context=context)
    else:
        return render(request, 'property_details.html', context=context)


def handle_query(request,current_property, current_user, id):

    new_enquiry = Enquiry()
    new_enquiry.enquiry_user = current_user
    new_enquiry.property = current_property
    new_enquiry.description = request.POST['query_area']
    new_enquiry.save()
    return redirect('propertyapp:existingproperty',id=id)


class CreateNewProperty(View):

    def get(self, request):
        if check_session(request,'logged_in','is_seller'):
            context={
                'property_form': NewPropertyForm(),
                'property_image': PropertyImagesForm()
            }
            return render(request, 'property_register.html', context=context)
        elif not check_session(request,'logged_in'):
            messages.add_message(request, messages.INFO, "Not Logged In, Please login as seller to post a property")
        return redirect('loginapp:check_login')

    def post(self,request):

        images_uploaded = self.request.FILES.getlist('Property_Images')
        form_data = NewPropertyForm(self.request.POST)
        if form_data.is_valid():
            property_form = form_data.save(commit=False)
            property_form.property_poster_id = self.request.user.id
            property_form.property_city = self.request.POST.get('select_city')
            property_form.property_states = self.request.POST.get('select_state')
            property_form.save()
            total_uploads = 5 if len(images_uploaded) > 5 else len(images_uploaded)
            for i in range(total_uploads):
                PropertyImages.objects.create(property_image=images_uploaded[i], property_name_id=property_form.id)
            return redirect('propertyapp:showfeaturedpage')
        else:
            return HttpResponse(form_data.errors)


class ExistingProperty(View):

    def get(self, request, id):
        property = Property.objects.get(pk=id)
        property_images = PropertyImages.objects.filter(property_name_id=property.id)
        no_of_images = len(property_images)
        current_user = request.session.get('current_user')
        property_poster = property.property_poster
        context = {'property': property, 'property_images': property_images, 'no_of_images': range(no_of_images)}
        if check_session(request,'logged_in'):
            context['logged_in'] = True
            is_buyer = not check_session(request, 'is_seller')
            if is_buyer:
                return show_property_for_buyer(request, context, current_user, property)
            else:
                return show_property_for_seller(request, context, current_user, property_poster)
            return render(request, 'property_details.html', context=context)

        return render(request, 'property_details.html', context=context)

    def post(self, request, id):
        current_property = Property.objects.get(pk=id)
        current_user_value = User.objects.get(username=request.session.get('current_user'))
        current_user = NewUser.objects.get(user=current_user_value)
        if self.request.POST.get('update_property'):

            images_uploaded = self.request.FILES.getlist('property_images')
            form_data = NewPropertyForm(self.request.POST)
            if form_data.is_valid():

                property_form = form_data.save(commit=False)
                property_form.property_poster_id = self.request.user.id

                for field in string_fields:
                    setattr(current_property, field, self.request.POST.get(field))
                for field in int_fields:
                    setattr(current_property, field, int(self.request.POST.get(field)))
                current_property.save()

                PropertyImages.objects.filter(property_name_id=current_property.id).delete()
                total_uploads = 5 if len(images_uploaded) > 5 else len(images_uploaded)
                for i in range(total_uploads):
                    PropertyImages.objects.create(property_image=images_uploaded[i], property_name_id=current_property.id)
                return HttpResponse('property created successfully')

            else:

                return HttpResponse(form_data.errors)

        elif request.POST.get('submit_query'):

            return handle_query(request, current_property, current_user,id)


class DeleteProperty(DeleteView):
    model = Property
    template_name = 'property_confirm_delete.html'
    success_url = reverse_lazy('userdashboardapp:userdashboard')


def search_property(request):
    print(request.POST.get('search_text'))
    city_search_results = Property.objects.filter(property_city=request.POST.get('select_city', ""))
    state_search_results = Property.objects.filter(property_states=request.POST.get('select_state', ""))
    query_result = city_search_results
    query_result = query_result.union(state_search_results)
    if request.POST.get('search_text') is not "":
        text_search_results = Property.objects.filter(property_title__icontains=request.POST.get('search_text'))
        query_result = query_result.union(text_search_results)
    return show_property(request, query_result)


def show_featured_page(request):

    p =[]
    p_images = []
    count = len(Property.objects.filter())
    indexes = [i for i in range(count,count-3,-1)]
    current_user=request.session.get('current_user', None)
    user_name=''
    if current_user is not None:
        user_name = User.objects.get(username = current_user).first_name
    for i in indexes:
        p.append(Property.objects.get(pk=i))
        image = PropertyImages.objects.filter(property_name_id=p[len(p)-1].id)[0]
        p_images.append(image)
    final_p = zip(p, p_images)
    return render(request, 'property_featured.html', {'property': p,
                                                      'property_images': p_images,
                                                      'range': range(1, 4),
                                                      'final_property': final_p,
                                                      'logged_in': request.session.get('logged_in', None),
                                                      'user_first_name':user_name,
                                                      'is_seller':request.session.get('is_seller', False)
                                                     })


def show_home_page(request):

    properties = Property.objects.all().order_by('-id')
    print(properties)
    return show_property(request, properties)


def show_property(request, property_set):
    property_images_set = []
    for property in property_set:
        property_images_set.append(PropertyImages.objects.filter(property_name_id=property.id)[0])
    display_properties = list(zip(property_set, property_images_set))
    page = request.GET.get('page')
    paginator = Paginator(display_properties, 6)
    final_properties = paginator.get_page(page)
    return render(request, 'property_home.html', {'properties': final_properties})
