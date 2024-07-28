from django.urls import re_path
from . import views
from favlinks import views as fav_views
from django.urls import path, include

urlpatterns = [
    re_path('login', views.login),
    re_path('signup', views.signup),
    re_path('test_token', views.test_token),
    path('api/', include('favlinks.urls'))
]
