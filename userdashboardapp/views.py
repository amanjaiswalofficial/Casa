from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from registerapp.models import NewUser


class UserDashboardApp(View):

    def get(self,request):
        return self.show_user()

    def show_user(self):
        username = self.request.session.get('current_user')
        try:
            current_user = NewUser.objects.get(username=username)
            user = {'user': current_user}
            is_seller = self.request.session.get('is_seller', False)
            if is_seller:
                return render(self.request, 'dashboard_seller.html', context=user)
            else:
                return render(self.request, 'dashboard_buyer.html', context=user)
        except NewUser.DoesNotExist:
            return redirect('loginapp:check_login')

    def post(self, request):
        username = self.request.session.get('current_user')
        current_user = NewUser.objects.get(username=username)
        if request.POST.get('update_profile_button'):
            return render(request,'update_user_form.html', {'user': current_user})
        elif request.POST.get('update_profile'):
            return redirect('registerapp:newuserview')