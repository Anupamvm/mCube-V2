"""mcube URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path,include
import f,o,p,r,a
from f import views
from o import views
from p import views
from a import views
from r import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', r.views.home, name='home'),
    path('f/', f.views.home, name='home'),
    path('o/', o.views.home, name='home'),

    path('p/', p.views.home, name='home'),
    path('p/login', p.views.login_view, name='login'),
    path('p/holdings', p.views.get_holdings_view, name='getholdings'),

    path('r/', r.views.home, name='home'),
    path('a/', a.views.home, name='home'),
]
