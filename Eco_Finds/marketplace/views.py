from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Review, CartItem
from django.contrib.auth import logout
from .forms import ReviewForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Order, UserHistory
from .forms import UserRegistrationForm
from .models import UserRegistration
from django.utils import timezone

def home(request):
    products = Product.objects.all()
    username = request.session.get('username', None)
    return render(request, 'marketplace/home.html', {'products': products, 'username': username})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                request.session['username'] = username
                request.session.set_expiry(180)  # Set session to expire in 3 minutes
                request.session['last_touch'] = timezone.now().timestamp()
                messages.info(request, f'You are now logged in as {username}.')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/Login.html', {'form': form})

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
    return render(request, 'marketplace/Products.html', {'product': product, 'reviews': reviews, 'review_form': review_form, 'username': request.session.get('username')})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
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
    messages.info(request, 'Your session has expired. Please log in again.')
    return redirect('login')

@login_required
def profile(request):
    user_orders = Order.objects.filter(user=request.user)
    history, created = UserHistory.objects.get_or_create(user=request.user)
    return render(request, 'marketplace/profile.html', {'user_orders': user_orders, 'history': history, 'username': request.session.get('username')})

def products(request):
    products = Product.objects.all()
    username = request.session.get('username', None)
    return render(request, 'marketplace/Products.html', {'products': products, 'username': username})

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
    return render(request, 'marketplace/cart.html', {'cart_items': cart_items, 'username': request.session.get('username')})

@login_required
def checkout(request):
    if request.method == 'POST':
        cart_items = CartItem.objects.filter(user=request.user)
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        order = Order.objects.create(
            user=request.user,
            total_price=total_price,
            shipping_address=request.POST['shipping_address'],
            shipping_city=request.POST['shipping_city'],
            shipping_pin=request.POST['shipping_pin'],
            billing_city=request.POST['billing_city'],
            billing_pin=request.POST['billing_pin'],
            billing_address=request.POST['billing_address']
        )
        order.items.set(cart_items)
        cart_items.delete()
        return redirect('awaiting_payment')
    return render(request, 'marketplace/checkout.html', {'username': request.session.get('username')})

@login_required
def awaiting_payment(request):
    return render(request, 'marketplace/card_details.html', {'username': request.session.get('username')})

@login_required
def card_details(request):
    payment_type = request.POST.get('payment')
    return render(request, 'marketplace/card_details.html', {'payment_type': payment_type, 'username': request.session.get('username')})

@login_required
def submit_payment(request):
    if request.method == 'POST':
        # Process the payment details here
        return redirect('order_success')
    return render(request, 'marketplace/card_details.html', {'username': request.session.get('username')})

@login_required
def order_success(request):
    return render(request, 'marketplace/order_success.html', {'username': request.session.get('username')})
