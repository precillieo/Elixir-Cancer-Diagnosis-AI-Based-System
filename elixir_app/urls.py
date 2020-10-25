from django.urls import path
from django.conf.urls import url
from django.conf import settings 
from django.conf.urls.static import static 
# from .views import *

from . import views

urlpatterns = [
    path('homepage/', views.elixir_dashboard,name="elixir_dashboard"),
    path('login/', views.elixir_login, name="elixir_login"),
    path('logout/', views.logoutUser, name="logoutUser"),
    path('predict/',views.PredictImage,name="predict")

    # path('', views.elixir_login,name='logpage'),
    # path('', views.elixir_dashboard,name='homepage'),
]
if settings.DEBUG: 
		urlpatterns += static(settings.MEDIA_URL, 
							document_root=settings.MEDIA_ROOT)