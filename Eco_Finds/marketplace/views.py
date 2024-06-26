from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Review, CartItem
from django.contrib.auth import logout
from .forms import ReviewForm
from .forms import UserRegisterForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Order, UserHistory


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
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})  # Pointing to standalone register.html


# def logout_view(request):
#     logout(request)
#     messages.info(request, 'You have successfully logged out.')
#     return redirect('home')


@login_required
def profile(request):
    user_orders = Order.objects.filter(user=request.user)
    history, created = UserHistory.objects.get_or_create(user=request.user)
    return render(request, 'marketplace/profile.html', {'user_orders': user_orders, 'history': history})



# New products view
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
        cart_items = CartItem.objects.filter(user=request.user)
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        order = Order.objects.create(
            user=request.user,
            total_price=total_price,
            shipping_address=request.POST['shipping_address'],
            billing_address=request.POST['billing_address']
        )
        order.items.set(cart_items)
        cart_items.delete()
        return redirect('order_success')
    return render(request, 'marketplace/checkout.html')

def order_success(request):
    return render(request, 'marketplace/order_success.html')
