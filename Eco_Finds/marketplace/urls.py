from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import card_details_view
from .views import forget_password, set_new_password, order_history
from .views import wishlist, add_to_wishlist, remove_from_wishlist, add_to_cart_from_wishlist, item_details
from .views import generate_invoice

urlpatterns = [
    path('', views.home, name='home'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('products/', views.products, name='products'),
    path('products/', views.product_showcase, name='product_showcase'),
    path('rewards/', views.rewards, name='rewards'),
    path('aboutus/', views.aboutus, name='aboutus'),
    # path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('awaiting_payment/', views.awaiting_payment, name='awaiting_payment'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('card-details/<str:card_type>/', card_details_view, name='card_details'),
    path('submit_payment/', views.submit_payment, name='submit_payment'),
    path('order_success/', views.order_success, name='order_success'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/favorite/<int:product_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('cart/update_quantity/<int:product_id>/<str:action>/', views.update_quantity, name='update_quantity'),
    path('forget_password/', forget_password, name='forget_password'),
    path('security_questions/', views.security_questions, name='security_questions'),
    path('set_new_password/', set_new_password, name='set_new_password'),
    path('apply_reward_points/', views.apply_reward_points, name='apply_reward_points'),
    path('wishlist/', wishlist, name='wishlist'),
    path('add-to-wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/add_to_cart/<int:product_id>/', add_to_cart_from_wishlist, name='add_to_cart_from_wishlist'),
    path('remove-from-wishlist/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('order_history/', order_history, name='order_history'),
    path('order/item-details/<int:item_id>/', item_details, name='item_details'),
    path('order/invoice/<int:order_id>/', generate_invoice, name='generate_invoice'),

    #  path('order-history/', views.order_history, name='order_history'),
    #  path('create-order/', views.create_order, name='create_order'),

]

