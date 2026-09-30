"""
URL configuration for core_config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from inquiries.views import dashboard_view 
from users.views import tailor_login_view

urlpatterns = [
    path('admin/', admin.site.urls),
    # Catch any accidental /accounts/login/ requests and route them to your login page
    path('accounts/login/', lambda request: redirect('login')),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('', include('users.urls')),
    path('portfolio/', include('portfolio.urls')),
    path('inquiries/', include(('inquiries.urls', 'inquiries'), namespace='inquiries')),
    path('tailor_login/', tailor_login_view, name='tailor_login'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

