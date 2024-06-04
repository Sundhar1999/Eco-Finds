# marketplace/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('products/', views.products, name='products'),
    path('register/', views.register, name='register'),
]
