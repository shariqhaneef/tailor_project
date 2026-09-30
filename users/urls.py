from django.urls import path
from django.contrib.auth import views as auth_views
from .views import RegisterView, home, login_view, logout_view, DashboardView

urlpatterns = [
    path('', home, name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    
    # Password Reset Routes
    path('reset_password/', 
         auth_views.PasswordResetView.as_view(template_name='users/password_reset_form.html'), 
         name='password_reset'),

    path('reset_password_sent/', 
         auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), 
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), 
         name='password_reset_confirm'),

    path('reset_password_complete/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), 
         name='password_reset_complete'),
]