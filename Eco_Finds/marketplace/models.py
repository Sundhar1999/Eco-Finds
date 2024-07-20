from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.utils import timezone

import os

def get_upload_path(instance, filename):
    # Get the category name, replace spaces with underscores and convert to lowercase
    category_name = instance.category.name.replace(" ", "_").lower()
    # Build the upload path
    return os.path.join('products', category_name, filename)


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to=get_upload_path)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    carbon_emission = models.PositiveIntegerField(help_text="Carbon emission reduction percentage")
    environmental_impact = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.name
    

class UserHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    visits = models.IntegerField(default=0)
    last_visit = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.visits} visits"
    

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"
    

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    is_favorite = models.BooleanField(default=False)

    @property
    def total_price(self):
        return self.product.price * self.quantity
    

    # def __str__(self):
    #     return self.product.price * self.quantity

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f'Cart ({self.user.username})'
    

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem)
    ordered_at = models.DateTimeField(auto_now_add=True)
    billing_address = models.CharField(max_length=255)
    shipping_address = models.CharField(max_length=255)
    product_name = models.CharField(max_length=255, default='default_product_name')

    def __str__(self):
        return f'Order #{self.id} by {self.user.username}'

    def get_total_price(self):
        return sum(item.total_price for item in self.items.all())

class Checkout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shipping_unit_no = models.CharField(max_length=100)
    shipping_street = models.CharField(max_length=200)
    shipping_city = models.CharField(max_length=100)
    shipping_pin = models.CharField(max_length=10)
    phone = models.CharField(max_length=15)
    payment_method = models.CharField(max_length=50)

    def __str__(self):
        return f'Checkout for {self.user.username}'
    

class CardDetails(models.Model):
    checkout = models.ForeignKey(Checkout, on_delete=models.CASCADE, default=1)
    card_type = models.CharField(max_length=50)
    card_number = models.CharField(max_length=20)
    expiry_date = models.CharField(max_length=5)
    cardholder_name = models.CharField(max_length=100)
    cvv = models.CharField(max_length=4)

    def __str__(self):
        return f'Card Details for {self.checkout.user.username}'
    

###LOCKED_DON'T TOUCH - IF U TOUCH, GA WILL GIVE 0.

class UserRegistration(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    security_question1 = models.CharField(max_length=255)
    security_answer1 = models.CharField(max_length=255)
    security_question2 = models.CharField(max_length=255)
    security_answer2 = models.CharField(max_length=255)
    wishlist = models.ManyToManyField('Product', blank=True, related_name='wishlisted_by')

    def __str__(self):
        return self.user.username
    
###LOCKED_DON'T TOUCH - IF U TOUCH, GA WILL GIVE 0.


class Reward(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    points_required = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# uname - sundhar
# pswd - sundhar@123


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    visit_count = models.IntegerField(default=0)
    last_visit = models.DateTimeField(null=True, blank=True)



def profile_view(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)

    # Check session for visit tracking
    session_key = f'profile_visited_{user.id}'
    if not request.session.get(session_key, False):
        profile.visit_count += 1
        profile.last_visit = now()
        profile.save()
        request.session[session_key] = True

    orders = Order.objects.filter(user=user)

    context = {
        'user': user,
        'profile': profile,
        'orders': orders
    }
    return render(request, 'profile.html', context)





# Uname - sundhark
# pswd - Will2win@1148

# uname - sundhar
# pswd - sundhar@123