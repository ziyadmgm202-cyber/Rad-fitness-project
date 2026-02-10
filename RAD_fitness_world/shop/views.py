from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth import logout,login,authenticate
from django.contrib import messages
from .models import Category


class HomeView(View):
    def get(self,request):
        catogories=Category.objects.all()
        return render(request,'index.html',{'catogories':catogories})
    
    
    
class Product(View):
    def get(self,request,i):
        b=Category.objects.get(id=i)
        return render(request,'productcollection.html',{'category':b})



from django.shortcuts import render, redirect
from django.views import View
from .forms import SignupForm, LoginForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


class SignupView(View):
    def get(self, request):
        form = SignupForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'signup successful')
            return redirect('login')
        return render(request, 'register.html', {'form': form})


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            u = form.cleaned_data['username']
            p = form.cleaned_data['password']
            user = authenticate(request, username=u, password=p)
            if user is None:
                messages.error(request, "invalid username or password")
                return redirect('login')
            login(request, user)
            messages.success(request, "Login successful")
            if user.is_superuser:
                return redirect('admin-dashboard')
            return redirect('home')
        else:
            messages.error(request, "form not valid")
            return redirect('login')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')



