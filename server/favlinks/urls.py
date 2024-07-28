from django.urls import path
from . import views

urlpatterns = [
    path('test_res/', views.check_res),
    path('create_category/', views.create_cat),
    path('list_category/', views.list_cats),
    path('list_tags/', views.list_tags),
    path('create_tag/', views.create_tag),
    path('create_favlink/', views.create_favorite_url),
    path('list_favlinks/', views.list_favorite_urls)
]