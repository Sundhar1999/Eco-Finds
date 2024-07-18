from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.hashers import make_password, check_password
from .models import Product, Review, CartItem, Reward, Category
from django.contrib.auth import logout
from .forms import ReviewForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Order, UserHistory, CardDetails, Checkout
from .forms import UserRegistrationForm, CheckoutForm, CardDetailsForm, RewardForm
from .forms import ForgetPasswordForm, SetNewPasswordForm
from .models import UserRegistration
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile
from django.http import JsonResponse


def home(request):
    products = Product.objects.all()
    bamboo_category = Category.objects.get(name="Bamboo_Products")
    bamboo_products = Product.objects.filter(category=bamboo_category)[:5]

    home_essentials_category = Category.objects.get(name="Home_Essentials")
    kids_section_category = Category.objects.get(name="Kids_Section")
    men_clothing_category = Category.objects.get(name="Men_Clothing")
    women_clothing_category = Category.objects.get(name="Women_Clothing")
    recycled_category = Category.objects.get(name="Recycled_Products")

    home_essentials = Product.objects.filter(category=home_essentials_category)
    kids_section = Product.objects.filter(category=kids_section_category)
    men_clothing = Product.objects.filter(category=men_clothing_category)
    women_clothing = Product.objects.filter(category=women_clothing_category)
    recycled_products = Product.objects.filter(category=recycled_category)

    username = request.session.get('username', None)

    context = {
        'products': products,
        'bamboo_products': bamboo_products,
        'home_essentials': home_essentials,
        'kids_section': kids_section,
        'recycled_products': recycled_products,
        'men_clothing': men_clothing,
        'women_clothing': women_clothing,
        'username': username,
    }

    return render(request, 'marketplace/home.html', context)

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
                request.session.set_expiry(300)  # Set session to expire in 3 minutes
                request.session['last_touch'] = timezone.now().timestamp()
                messages.info(request, f'You are now logged in as {username}.')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})



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
            print(form.errors)  # For debugging purposes
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


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
    category_name = request.GET.get('category', None)
    if category_name:
        products = Product.objects.filter(category__name=category_name)
    else:
        products = Product.objects.all()

    categories = Category.objects.all()
    username = request.session.get('username', None)
    return render(request, 'marketplace/Products.html', {
        'products': products,
        'categories': categories,
        'username': username,
        'category_name': category_name
    })



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
    total_price = sum(item.total_price for item in cart_items)
    return render(request, 'marketplace/cart.html', {'items': cart_items, 'total_price': total_price})

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


def forget_password(request):
    if request.method == 'POST':
        form = ForgetPasswordForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            try:
                user_registration = UserRegistration.objects.get(user__username=username)
                request.session['username'] = username
                request.session['security_question1'] = user_registration.security_question1
                request.session['security_question2'] = user_registration.security_question2
                return redirect('security_questions')
            except UserRegistration.DoesNotExist:
                messages.error(request, "Username does not exist.")
    else:
        form = ForgetPasswordForm()
    return render(request, 'registration/forget_password.html', {'form': form})


def security_questions(request):
    if request.method == 'POST':
        username = request.session.get('username')
        answer1 = request.POST.get('security_answer1')
        answer2 = request.POST.get('security_answer2')
        try:
            user_registration = UserRegistration.objects.get(user__username=username)
            if user_registration.security_answer1 == answer1 and user_registration.security_answer2 == answer2:
                return redirect('set_new_password')
            else:
                messages.error(request, "Security answers do not match our records.")
                return redirect('forget_password')
        except UserRegistration.DoesNotExist:
            messages.error(request, "User does not exist.")
            return redirect('forget_password')
    else:
        security_questions = {
            'question1': request.session.get('security_question1'),
            'question2': request.session.get('security_question2')
        }
    return render(request, 'registration/security_questions.html', {'security_questions': security_questions})


def set_new_password(request):
    if request.method == 'POST':
        form = SetNewPasswordForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            new_password = form.cleaned_data['new_password']
            confirm_password = form.cleaned_data['confirm_password']

            if new_password != confirm_password:
                messages.error(request, "Passwords do not match.")
                return render(request, 'registration/set_new_password.html', {'form': form, 'username': username})

            try:
                user_registration = UserRegistration.objects.get(user__username=username)
                user = user_registration.user
                user.set_password(new_password)  # Use set_password method to hash the password
                user.save()
                messages.success(request, "Password reset successful. Please log in with your new password.")
                return redirect('login')
            except UserRegistration.DoesNotExist:
                messages.error(request, "User does not exist.")
                return redirect('forget_password')
    else:
        form = SetNewPasswordForm()
        username = request.session.get('username')
    return render(request, 'registration/set_new_password.html', {'form': form, 'username': username})


@login_required
def awaiting_payment(request):
    return render(request, 'marketplace/card_details.html', {'username': request.session.get('username')})

@login_required
def card_details_view(request, card_type):
    if request.method == 'POST':
        form = CardDetailsForm(request.POST)
        if form.is_valid():
            card_details = form.save(commit=False)
            card_details.user = request.user
            card_details.save()
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
        
        return redirect('order_success')
    return render(request, 'marketplace/card_details.html', {'username': request.session.get('username')})

@login_required
def order_success(request):
    return render(request, 'marketplace/order_success.html', {'username': request.session.get('username')})

def aboutus(request):  
    return render(request, 'marketplace/aboutus.html')


######REWARDS

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



@login_required
def wishlist(request):
    user_registration = request.user.userregistration
    wishlist_items = user_registration.wishlist.all()
    return render(request, 'marketplace/partials/wishlist_items.html', {'wishlist_items': wishlist_items})



@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    return render(request, 'cart.html', {'cart_items': cart_items})

# @login_required
# def add_to_cart(request, product_id):
#     product = get_object_or_404(Product, id=product_id)
#     cart, created = Cart.objects.get_or_create(user=request.user)
#     cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
#     if not created:
#         cart_item.quantity += 1
#         cart_item.save()
#     return redirect('view_cart')

@login_required
def add_to_cart(request, product_id):
    print(f"Adding product {product_id} to cart")
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        print(f"Incrementing quantity for product {product_id}")
        cart_item.save()
    else:
        cart_item.save()
        print(f"Added product {product_id} to cart")
    return redirect('cart')

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
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    user_registration = request.user.userregistration
    user_registration.wishlist.add(product)
    return JsonResponse({'success': True})

@login_required
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    user_registration = request.user.userregistration
    user_registration.wishlist.remove(product)
    return redirect('home')

@login_required
def add_to_cart_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    user_registration = request.user.userregistration
    # Add product to cart logic here
    user_registration.wishlist.remove(product)
    return JsonResponse({'success': True})
    # return redirect('cart')


def cart_view(request):
    try:
        cart = Cart.objects.get(user=request.user)
        items = CartItem.objects.filter(cart=cart)
        total_price = sum(item.get_total_price() for item in items)
    except Cart.DoesNotExist:
        cart = None
        items = []
        total_price = 0

    context = {
        'cart': cart,
        'items': items,
        'total_price': total_price
    }
    return render(request, 'cart.html', context)

@login_required
def profile_view(request):
    profile = UserRegistration.objects.get(user=user)
    orders = Order.objects.filter(user=request.user)
    return render(request, 'profile.html', {'user': request.user, 'profile': profile, 'orders': orders})

# to ensure that a Profile object is created whenever a new user is registered
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userregistration.save()

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                # Get or create UserRegistration instance
                user_registration, created = UserRegistration.objects.get_or_create(user=user)
                # Update visit count and last visit time
                user_registration.visit_count += 1
                user_registration.last_visit = timezone.now()
                user_registration.save()
                return HttpResponseRedirect(reverse('myapp:index'))
            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login details.')
    else:
        return render(request, 'registration/login.html')

@login_required
def view_profile(request):
    user_registration = UserRegistration.objects.get(user=request.user)
    orders = Order.objects.filter(user=request.user)
    return render(request, 'marketplace/profile.html', {'user_registration': user_registration})

def product_showcase(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    return render(request, 'marketplace/Products.html', {
        'categories': categories,
        'products': products
    })