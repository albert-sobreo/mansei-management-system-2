from django.core.exceptions import NON_FIELD_ERRORS
from django.http.response import JsonResponse
from django.shortcuts import redirect, render, HttpResponse
from django.views import View
from ..forms import *
from django.contrib.auth import authenticate, login as auth_login, logout
from ..models import *

##### CLASS-BASED VIEWS #####
class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/')
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            if user.authLevel == 'dtr':
                return redirect('/ems-dtr/')
            return redirect('/')
        else:
            return HttpResponse(user)

class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        form = RegisterForm(request.POST or None, request.FILES or NON_FIELD_ERRORS)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Account Successfully Registered. Wait for the admin to approve your registration.'})
        else:
            return render(request, 'register.html', {"forms": form})

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('/')

class RegisterApprovalView(View):
    def get(self, request):
        context = {
            'register' : Register.objects.all()
        }
        return render(request, 'register-approval.html', context)
        
    def post(self, request):
        pk = request.POST['pk']
        register = Register.objects.get(pk=pk)

        user = User()
        user.first_name = register.first_name
        user.last_name = register.last_name
        user.username = register.username
        user.email = register.email
        user.password = register.password
        user.department = register.department
        user.save()
        register.delete()

        return redirect('/register-approval/')
