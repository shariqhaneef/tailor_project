from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout 
from django.contrib.auth.decorators import login_required
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from inquiries.models import Inquiry

class RegisterView(View):

    def get(self, request):
        register_form = UserCreationForm()
        # Changed 'views/register.html' to 'users/register.html' to match your folder structure
        return render(request, 'users/register.html', {'register_form': register_form})
    
    def post(self, request):
        register_form = UserCreationForm(data=request.POST)
        if register_form.is_valid():
            user = register_form.save()
            login(request, user)
            messages.success(request, f'User {user.username} registered successfully.')
            return redirect('login')  # <-- Redirects to login page for now
        else:
            messages.error(request, 'An error occurred trying to register.')
            return render(request, 'users/register.html', {'register_form': register_form})


def home(request):
    return render(request, 'users/home.html')

def login_view(request):
    if request.method == 'POST':
       login_form = AuthenticationForm(request=request, data=request.POST)
       if login_form.is_valid():
           username = login_form.cleaned_data.get('username')
           password = login_form.cleaned_data.get('password')
           user = authenticate(request, username=username, password=password)
           if user is not None :
               login(request, user)
               messages.success(
                   request, f'You are now logged in as {username}.')
               return redirect('home')
           else: 
             messages.error(request, f'An error occured trying to login.')
       else:
            messages.error(request, 'An error occurred trying to login.')
    elif request.method == 'GET': 
        login_form = AuthenticationForm()
    return render(request, 'users/login.html', {'login_form': login_form})

def logout_view(request):
    logout(request)
    return redirect('home')

class DashboardView(LoginRequiredMixin, ListView):
    model = Inquiry
    template_name = 'users/dashboard.html'
    context_object_name = 'orders' # This is the word we will use in the HTML loop
    login_url = 'login' # If a guest tries to visit, send them to the login page

    def get_queryset(self):
        # This grabs ONLY the orders belonging to the currently logged-in user
        return Inquiry.objects.filter(customer=self.request.user).order_by('-created_at')


def tailor_login_view(request):
    if request.method == 'POST':
        username_input = request.POST.get('username')
        password_input = request.POST.get('password')
        
        user = authenticate(request, username=username_input, password=password_input)
        
        if user is not None:
            if user.is_staff:
                login(request, user)
                messages.success(request, f'Welcome back, Master {user.get_full_name() or user.username}. Cutting room workbench active.')
                return redirect('dashboard')
            else:
                messages.error(request, 'Access Denied: This portal is restricted to verified Atelier Tailors.')
        else:
            messages.error(request, 'Invalid atelier credentials. Please check your username and password.')
            
    return render(request, 'users/tailor_login.html')
    