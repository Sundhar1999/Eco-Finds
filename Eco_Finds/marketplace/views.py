from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Review, CartItem
from django.contrib.auth import logout
from .forms import ReviewForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Order, UserHistory, CardDetails, Checkout
from .forms import UserRegistrationForm, CheckoutForm, CardDetailsForm
from .models import UserRegistration
from django.contrib.auth.hashers import make_password


def home(request):
    products = Product.objects.all()
    return render(request, 'marketplace/home.html', {'products': products})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f'You are now logged in as {username}.')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'marketplace/Login.html', {'form': form})


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = product.reviews.all()
    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.product = product
            review.save()
            return redirect('product_detail', product_id=product.id)
    else:
        review_form = ReviewForm()
    return render(request, 'marketplace/Products.html', {'product': product, 'reviews': reviews, 'review_form': review_form})


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/Register.html', {'form': form})



def logout_view(request):
    logout(request)
    messages.info(request, 'You have successfully logged out.')
    return redirect('home')


@login_required
def profile(request):
    user_orders = Order.objects.filter(user=request.user)
    history, created = UserHistory.objects.get_or_create(user=request.user)
    return render(request, 'marketplace/profile.html', {'user_orders': user_orders, 'history': history})


def products(request):
    products = Product.objects.all()
    return render(request, 'marketplace/Products.html', {'products': products})


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')


@login_required
def cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    return render(request, 'marketplace/cart.html', {'cart_items': cart_items})


@login_required
def checkout(request):
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            checkout = form.save(commit=False)
            checkout.user = request.user
            checkout.save()
            selected_card_type = form.cleaned_data['payment_method']
            return redirect('card_details', card_type=selected_card_type)
    else:
        form = CheckoutForm()
    return render(request, 'marketplace/checkout.html', {'form': form})

# @login_required
# def checkout(request):
#     if request.method == 'POST':
#         form = CheckoutForm(request.POST)
#         if form.is_valid():
#             selected_card_type = form.cleaned_data['payment_method']
#             return redirect('card_details', card_type=selected_card_type)
#     else:
#         form = CheckoutForm()
#     return render(request, 'marketplace/checkout.html', {'form': form})

@login_required
def card_details_view(request, card_type):
    if request.method == 'POST':
        form = CardDetailsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('order_success')
    else:
        form = CardDetailsForm(initial={'card_type': card_type})
    return render(request, 'marketplace/card_details.html', {'form': form})

@login_required
def order_success(request):
    return render(request, 'marketplace/order_success.html')

@login_required
def awaiting_payment(request):
    return render(request, 'marketplace/card_details.html')

# @login_required
# def card_details(request):
#     if request.method == 'POST':
#         form = CardDetailsForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('order_success')
#     else:
#         form = CardDetailsForm()
#     return render(request, 'marketplace/card_details.html', {'form': form})

@login_required
def submit_payment(request):
    if request.method == 'POST':
        # Process the payment details here
        return redirect('order_success')
    return render(request, 'marketplace/card_details.html')


@login_required
def order_success(request):
    return render(request, 'marketplace/order_success.html')

