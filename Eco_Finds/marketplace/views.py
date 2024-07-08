from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Review, CartItem, Reward, Cart
from django.contrib.auth import logout
from .forms import ReviewForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Order, UserHistory, CardDetails, Checkout
from .forms import UserRegistrationForm, CheckoutForm, CardDetailsForm, RewardForm
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
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('view_cart')

@login_required
def remove_from_cart(request, product_id):
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, product__id=product_id)
    cart_item.delete()
    return redirect('view_cart')


@login_required
def toggle_favorite(request, product_id):
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, product__id=product_id)
    cart_item.is_favorite = not cart_item.is_favorite
    cart_item.save()
    return redirect('view_cart')

@login_required
def update_quantity(request, product_id, action):
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, product__id=product_id)
    if action == 'increase':
        cart_item.quantity += 1
    elif action == 'decrease' and cart_item.quantity > 1:
        cart_item.quantity -= 1
    cart_item.save()
    return redirect('view_cart')
@login_required
def cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    return render(request, 'marketplace/cart.html', {'cart_items': cart_items, 'username': request.session.get('username')})

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

    #     cart_items = CartItem.objects.filter(user=request.user)
    #     total_price = sum(item.product.price * item.quantity for item in cart_items)
    #     order = Order.objects.create(
    #         user=request.user,
    #         total_price=total_price,
    #         shipping_address=request.POST['shipping_address'],
    #         shipping_city=request.POST['shipping_city'],
    #         shipping_pin=request.POST['shipping_pin'],
    #         billing_city=request.POST['billing_city'],
    #         billing_pin=request.POST['billing_pin'],
    #         billing_address=request.POST['billing_address']
    #     )
    #     order.items.set(cart_items)
    #     cart_items.delete()
    #     return redirect('awaiting_payment')
    # return render(request, 'marketplace/checkout.html', {'username': request.session.get('username')})

@login_required
def awaiting_payment(request):
    return render(request, 'marketplace/card_details.html', {'username': request.session.get('username')})

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

def aboutus(request):  # For aboutus
    return render(request, 'aboutus.html')
@login_required
def rewards(request):
    # Calculate the total amount spent by the user
    user_orders = Order.objects.filter(user=request.user)
    total_spent = sum(order.total_price for order in user_orders)

    # Calculate the total reward points (0.5 points per dollar spent)
    total_points = total_spent * 0.5

    points_value = total_points * 2

    # Get the user's rewards
    rewards = Reward.objects.all()

    return render(request, 'marketplace/rewards.html', {
        'rewards': rewards,
        'total_points': total_points,
        'points_value': points_value,
    })



# @login_required
# def add_reward(request):
#     if request.method == 'POST':
#         form = RewardForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('rewards')
#     else:
#         form = RewardForm()
#     return render(request, 'marketplace/add_reward.html', {'form': form})
# return render(request, 'marketplace/order_success.html', {'username': request.session.get('username')})
