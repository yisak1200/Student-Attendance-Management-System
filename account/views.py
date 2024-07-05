from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth import logout
class LoginView(View):
    def get(self,request):
        return render(request,'account_templates/login.html')
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_obj = authenticate(request, username=username, password=password)
        if user_obj is not None:
            if user_obj.groups.filter(name='Manager').exists():
                login(request, user_obj)
                return redirect('manager_index')
            else:
                messages.error(request, "This user Group can't login in this page")
                return redirect('login_page')
        messages.error(request, 'Invalid username or password')
        return redirect('login_page')
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login_page')
        