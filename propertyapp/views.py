from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect, render, render_to_response
from django.template import RequestContext
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DeleteView, UpdateView
from registerapp.models import NewUser
from .forms import NewPropertyForm, PropertyImagesForm
from .models import PropertyImages, Property, Enquiry
from django.contrib import messages
from django.core.paginator import Paginator
from Casa.settings import EMAIL_ADDRESS, PASSWORD
import smtplib
import re

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
    """checks for the given session value in args and returns True or False"""

    flag = True
    for arg in args:
        flag = flag and request.session.get(arg, False)
    return flag


def show_property_for_buyer(request,context, current_user, current_property):
    """display property for buyer depending whether he has made query on it or not"""

    context['is_not_seller'] = True
    current_user = User.objects.get(username=current_user)
    try:
        Enquiry.objects.get(property=current_property, enquiry_user=current_user)
        return render(request, 'property_details.html', context=context)
    except Enquiry.DoesNotExist:
        context['no_query_made'] = True
        return render(request, 'property_details.html', context=context)


def show_property_for_seller(request, context, current_user, property_poster):
    """displays property to seller and opens the property in update mode if seller posted the property"""

    if current_user == str(property_poster):
        return redirect('propertyapp:updateproperty', pk=context['property'].id)
    else:
        return render(request, 'property_details.html', context=context)


def handle_query(request,current_property, current_user, id):
    """handles the query entered by the buyer about a property to send the mail to the user"""

    new_enquiry = Enquiry()
    new_enquiry.enquiry_user = current_user
    new_enquiry.property = current_property
    new_enquiry.description = request.POST['query_area']
    property_seller_email = NewUser.objects.get(user=new_enquiry.property.property_poster).email_field
    new_enquiry.save()
    # try:
    #     server = smtplib.SMTP('smtp.gmail.com:587')
    #     server.ehlo()
    #     server.starttls()
    #     server.login(EMAIL_ADDRESS, PASSWORD)
    #     new_enquiry.description = "You have a query for one of your properties,following are the details:\n" \
    #                               "Buyer's email: {}\n"\
    #                               "Buyer's phone: {}\n"\
    #                               "Query: {}".format(new_enquiry.enquiry_user.email_field,
    #                                                  new_enquiry.enquiry_user.phone_number,
    #                                                  new_enquiry.description)
    #     message = 'Subject: {}\n\n{}'.format(new_enquiry.property.property_title, new_enquiry.description.encode('utf-8'))
    #     server.sendmail(EMAIL_ADDRESS, 'amanjai01@gmail.com', message)
    #     server.quit()
    #     print("Success: Email sent!")
    # except:
    #     return HttpResponse("Email failed to send.")

    return redirect('propertyapp:existingproperty', id=id)


class CreateNewProperty(View):
    """Contains methods to create a new property"""

    def get(self, request):
        """return the form to post the new property"""

        if check_session(request, 'logged_in', 'is_seller'):
            context={
                'property_form': NewPropertyForm(),
                'property_image': PropertyImagesForm()
            }
            return render(request, 'property_register.html', context=context)
        elif not check_session(request,'logged_in'):
            messages.add_message(request, messages.INFO, "Not Logged In, Please login as seller to post a property")
        return redirect('loginapp:check_login')

    def post(self,request):
        """accepts the data from the seller and saves into the model if valid else return error"""

        form_data = NewPropertyForm(self.request.POST)
        form_images = PropertyImagesForm(self.request.FILES)
        images_uploaded = self.request.FILES.getlist('Property_Images')
        for images in images_uploaded:
            if re.match('^[\d\w.\-]*(.jpg|.png)$', str(images)) is None:
                return render(request, 'property_register.html', {'property_form': form_data,
                                                                  'property_image': form_images,
                                                                  'errors': True, 'image_error':\
                                                                  'Please ensure you have uploaded\
                                                                   image and nothing else'})

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
            return render(request, 'property_register.html', {'property_form': form_data,
                                                              'property_image': form_images,
                                                              'errors': True})


class ExistingProperty(View):
    """class handling requests made on existing properties, depending on user open in view or update mode"""

    def get(self, request, id):
        """
        :param request: request variable used
        :param id: to know which property is tried to be accessed
        :return: either the HTML page containing the property, or redirect to a method based on user logged in
        """
        try:
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
                # return render(request, 'property_details.html', context=context)

            return render(request, 'property_details.html', context=context)
        except Property.DoesNotExist:
            return render(request,'property_not_found.html')

    def post(self, request, id):
        """
        Method to call handle_query method with necessary parameters to save
        :param request: request variable used
        :param id: to know which property is being updated
        :return: response to handle_query method
        """
        if request.POST.get('submit_query'):
            current_property = Property.objects.get(pk=id)
            current_user_value = User.objects.get(username=request.session.get('current_user'))
            current_user = NewUser.objects.get(user=current_user_value)
            return handle_query(request, current_property, current_user, id)


class UpdateProperty(UpdateView):

    model = Property
    form_class = NewPropertyForm
    template_name = 'property_form.html'

    def get(self, request, *args, **kwargs):
        """
        Method to handle and decide whether allowing the logged in user to update the property or not
        :return: Either the form containing values to update the properties or login page to login as seller
        """

        if self.request.session.get('logged_in', False):

            current_property = Property.objects.get(pk=self.get_object().id)
            current_user = User.objects.get(username=self.request.session.get('current_user'))
            if current_property.property_poster == current_user:
                return super().get(request, *args, **kwargs)
            else:
                logout(self.request)
                messages.add_message(self.request, messages.INFO, "Please login as seller to update/delete a property")
                return redirect('loginapp:check_login')
        else:
            messages.add_message(self.request, messages.INFO,
                                 "Not Logged In, Please login as seller to update/delete a property")
            return redirect('loginapp:check_login')

    def get_context_data(self,*args, **kwargs):
        """
        Initialize the data to be sent to the HTML page
        :return: context to be used by the Django Template
        """
        current_property = Property.objects.get(pk=self.get_object().id)
        context = super(UpdateProperty, self).get_context_data(**kwargs)
        context['cities'] = ['Kanpur','New Delhi','Ghaziabad','Chandigarh']
        context['states'] = ['Uttar Pradesh', 'Delhi', 'Karnataka', 'Punjab']
        context['property_images'] = PropertyImages.objects.filter(property_name=current_property)
        return context

    def form_valid(self, form):
        """
        If the form data is valid, update the property
        :param form: from the template
        :return: on successful updation redirects to dashboard
        """
        form.instance.property_city = form.data['select_city']
        form.instance.property_state = form.data['select_state']
        form.instance.save()
        current_property =Property.objects.get(pk=self.get_object().id)
        if self.request.FILES:
            images = self.request.FILES.getlist('images')
            for image in images:
                if re.match('^[\d\w.\-]*(.jpg|.png)$', str(image)) is None:
                    context = self.get_context_data()
                    context['image_error'] = 'Please ensure you have uploaded image and nothing else'
                    return render(self.request, self.template_name, context=context)
            for image in images:
                current_image = PropertyImages.objects.filter(property_name=current_property)[images.index(image)]
                current_image.property_image = image
                current_image.save()
        return redirect('userdashboardapp:userdashboard')

    def form_invalid(self, form, *args, **kwargs):
        """

        :param form:
        :return: an HttpResponse to a page listing the error
        """
        context = self.get_context_data()
        return render(self.request, self.template_name, context=context)


class DeleteProperty(DeleteView, LoginRequiredMixin):
    """Class responsible to delete a property created by seller"""

    model = Property
    template_name = 'property_confirm_delete.html'
    success_url = reverse_lazy('userdashboardapp:userdashboard')

    def get(self, request, *args, **kwargs):
        """
        Method to handle and decide whether allowing the logged in user to delete the property or not
        :return: Either the form containing values to update the properties or login page to login as seller
        """
        if self.request.session.get('logged_in', False):

            current_property = Property.objects.get(pk=self.get_object().id)
            current_user = User.objects.get(username=self.request.session.get('current_user'))
            if current_property.property_poster == current_user:
                return super().get(request, *args, **kwargs)
            else:
                logout(self.request)
                messages.add_message(self.request, messages.INFO, "Please login as appropriate seller to \
                                                                    update/delete a property")
                return redirect('loginapp:check_login')
        else:
            messages.add_message(self.request, messages.INFO,
                                 "Not Logged In, Please login as seller to update/delete a property")
            return redirect('loginapp:check_login')


def search_property(request):
    """
    :param request: request variable used
    :return: the result set containing all the properties depending on the filter to a method to display them
    """
    invalid_entries = [' ', '', ""]
    if request.POST.get('select_city') is None or 'All Cities':
        city_search_results = Property.objects.all()
    else:
        city_search_results = Property.objects.filter(property_city=request.POST.get('select_city', ""))
    if request.POST.get('select_state') is None or 'All States':
        state_search_results = Property.objects.all()
    else:
        state_search_results = Property.objects.filter(property_states=request.POST.get('select_state', ""))
    query_result = city_search_results
    query_result = query_result.union(state_search_results)
    if request.POST.get('search_text') not in invalid_entries:
        text_search_results = Property.objects.filter(property_title__icontains=request.POST.get('search_text'))
        query_result = query_result.intersection(text_search_results)
    return show_property(request, query_result)


def show_featured_page(request):
    """
    Finds the top 3 properties from Property and send them to display
    :param request:
    :return: top 3 properties to display on the featured page
    """
    if request.method == 'GET':
        p_images = []
        count = len(Property.objects.filter())
        indexes = [i for i in range(count,count-3,-1)]
        current_user=request.session.get('current_user', None)
        user_name=''
        if current_user is not None:
            user_name = User.objects.get(username=current_user).first_name
        p = list(Property.objects.all().order_by('-id')[:3])
        for property in p:
            p_images.append(PropertyImages.objects.filter(property_name_id=property.id)[0])
        final_p = zip(p, p_images)
        return render(request, 'property_featured.html', {'property': p,
                                                          'property_images': p_images,
                                                          'range': range(1, 4),
                                                          'final_property': final_p,
                                                          'logged_in': request.session.get('logged_in', None),
                                                          'user_first_name': user_name,
                                                          'is_seller': request.session.get('is_seller', False)
                                                         })
    elif request.method == 'POST':
        return search_property(request)


def show_home_page(request):
    """
    Function to handle the home page request
    :param request:
    :return: the HTML page containing all the properties showing 6 at a time
    """

    properties = Property.objects.all().order_by('-id')
    print(properties)
    return show_property(request, properties)


def show_property(request, property_set):
    """
    Display the properties in a paginated manner
    :param request:
    :param property_set: the set of properties to display
    :return: the HTML page containing the given property and their images
    """

    property_images_set = []
    for property in property_set:
        property_images_set.append(PropertyImages.objects.filter(property_name_id=property.id)[0])
    display_properties = list(zip(property_set, property_images_set))
    page = request.GET.get('page')
    paginator = Paginator(display_properties, 6)
    final_properties = paginator.get_page(page)
    return render(request, 'property_home.html', {'properties': final_properties})


def handle_error(request, *args, **argv):
    response = render_to_response('property_not_found.html')
    response.status_code = 404
    return response
