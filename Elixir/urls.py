"""Elixir URL Configuration 

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf.urls import url
from elixir_app import views
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
from elixir_app.urls import urlpatterns as elixir_url
from django.urls import path, include 


urlpatterns = [
    # path('elixir_app/',include('elixir_app.urls')),
    # path('admin/', admin.site.urls),
    path('admin/', admin.site.urls),
    url('^$', views.elixir_login, name='logpage'),
    url(r'^homepage/', include(elixir_url) ),
] 
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)