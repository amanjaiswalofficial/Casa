import smtplib
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_list_or_404
from django.views import View
from django.views.generic import UpdateView
from Casa.settings import EMAIL_ADDRESS, PASSWORD
from propertyapp.views import handle_error
from registerapp.models import NewUser
from propertyapp.models import Enquiry, Property, PropertyImages
from django.contrib import messages
from userdashboardapp.models import QueryResponses
from .forms import NewUserUpdateForm


class UserDashboardApp(View):
    """Contains methods to show dashboard to the user, differentiates according to the type of user logged in"""

    def get(self,request):
        """calls the method show_user to check which user has logged in"""
        return self.show_user()

    def show_user(self):
        """If buyer has logged in, calls method for buyer dashboard, else calls for seller's dashboard"""
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
        """
        Displays the seller's dashboard
        :param current_user: to know which user has logged in
        :param context: containing information about current session
        :return: django template for the seller's dashboard
        """
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
        """
        Display the dashboard for the buyer
        :param current_user: to know which user has logged in
        :param context: extra information about the user
        :return: template for the buyer's dashboard
        """
        queries_made = []
        try:
            queries_made = get_list_or_404(Enquiry, enquiry_user=current_user)
        except Http404:
            queries_made = False
        finally:
            context['queries_made'] = queries_made
            return render(self.request, 'dashboard_buyer.html', context=context)

    def post(self, request):
        """
        Handles various button clicks over the dashboard like updating profile and sending query replies for seller
        :return: control to the method containing logic depending on user interaction
        """
        username = self.request.session.get('current_user')
        current_user = NewUser.objects.get(username=username)
        if request.POST.get('update_profile_button'):
            return UpdateUser.as_view()(request, pk=current_user.id)
        elif request.POST.get('update_profile'):
            return UpdateUser.as_view()(request, pk=current_user.id)
        elif request.POST.get('submit_response'):
            query_response = QueryResponses()
            enquiry_user = request.POST.get('enquiry_user')
            enquiry_property = request.POST.get('enquiry_property')
            current_enquiry = Enquiry.objects.filter(enquiry_user__email_field=enquiry_user, property__property_title=enquiry_property)[0]
            query_response.enquiry_made = current_enquiry
            query_response.response = request.POST.get('response_area')
            query_response.save()
            seller_email = NewUser.objects.get(user=request.user).email_field
            buyer_email = current_enquiry.enquiry_user.email_field
            print(buyer_email)
            # try:
            #     server = smtplib.SMTP('smtp.gmail.com:587')
            #     server.ehlo()
            #     server.starttls()
            #     server.login(EMAIL_ADDRESS, PASSWORD)
            #     description = "You have a response to one of your queries,following are the details:\n" \
            #                   "Property: {}\n" \
            #                   "Property Seller's Email: {}\n" \
            #                   "Response: {}".format(enquiry_property,
            #                                         seller_email,
            #                                         query_response.response)
            #     message = 'Subject: {}\n\n{}'.format(enquiry_property, description)
            #     server.sendmail(EMAIL_ADDRESS, 'amanjai01@gmail.com', message)
            #     server.quit()
            #     print("Success: Email sent!")
            # except:
            #     return HttpResponse("Email failed to send.")
            return redirect('userdashboardapp:userdashboard')


class UpdateUser(UpdateView):
    """
    Methods for enabling user to update his profile with some of the details
    """
    model = NewUser
    form_class = NewUserUpdateForm
    template_name = 'update_user.html'

    def get(self, request, *args, **kwargs):
        """
        Method to handle and decide whether allowing the logged in user to update the property or not
        :return: Either the form containing values to update the properties or login page to login as seller
        """
        if self.request.session.get('logged_in', False):
                return super().get(request, *args, **kwargs)
        else:
                messages.add_message(self.request, messages.INFO, "Please login as seller to post a property")
                return redirect('loginapp:check_login')

    def get_context_data(self, **kwargs):
        """
        Send some extra data to the form output
        :param kwargs:
        :return: context
        """
        context = super(UpdateUser, self).get_context_data(**kwargs)
        username = self.request.session.get('current_user')
        current_user = NewUser.objects.get(username=username)
        context['current_user'] = current_user
        return context

    def form_valid(self, form):
        """
        If the form data is valid, update the particular record
        :param form: data from the template
        :return: control to user dashboard
        """
        context = self.get_context_data()
        form.instance.is_seller = context['current_user'].is_seller
        form.instance.save()
        return redirect('userdashboardapp:userdashboard')


class UserQueryResponses(View):
    """
    An extra option at buyer's navbar, directing to a page containing all the responses made by seller's of respective\
    properties regarding the enquiry made by the buyer
    """
    def get(self, request):
        """
        Get all the responses made by the seller to display
        :param request:
        :return:
        """
        if request.session.get('logged_in'):
            if request.session.get('is_seller'):
                return handle_error(request)
            elif not request.session.get('is_seller', False):
                try:
                    queries = []
                    query_responses = []
                    enquiry_made = Enquiry.objects.filter(enquiry_user=self.request.user)
                    for enquiry in enquiry_made:
                        queries.append(QueryResponses.objects.filter(enquiry_made=enquiry))
                    for query in queries:
                        for responses in query:
                            query_responses.append(responses)
                except Enquiry.DoesNotExist:
                    query_responses = False
                except QueryResponses.DoesNotExist:
                    query_responses = False
                return render(request, 'query_response.html', {'query_responses': query_responses})
        else:
            return redirect('loginapp:check_login')

