from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import card_details_view

urlpatterns = [
    path('', views.home, name='home'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('products/', views.products, name='products'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('awaiting_payment/', views.awaiting_payment, name='awaiting_payment'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('card-details/<str:card_type>/', card_details_view, name='card_details'),
    path('submit_payment/', views.submit_payment, name='submit_payment'),
    path('order_success/', views.order_success, name='order_success'),
]

