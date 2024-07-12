from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    category = models.CharField(max_length=100)
    carbon_emission = models.TextField()
    environmental_impact = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

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


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Cart ({self.user.username})'

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.quantity} of {self.product.name}'

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    ordered_at = models.DateTimeField(auto_now_add=True)
    billing_address = models.CharField(max_length=255)
    shipping_address = models.CharField(max_length=255)

    def __str__(self):
        return f'Order #{self.id} by {self.user.username}'

class Checkout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shipping_unit_no = models.CharField(max_length=100)
    shipping_street = models.CharField(max_length=200)
    shipping_city = models.CharField(max_length=100)
    shipping_pin = models.CharField(max_length=10)
    phone = models.CharField(max_length=15)
    billing_unit_no = models.CharField(max_length=100, blank=True, null=True)
    billing_street = models.CharField(max_length=200, blank=True, null=True)
    billing_city = models.CharField(max_length=100, blank=True, null=True)
    billing_pin = models.CharField(max_length=10, blank=True, null=True)
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


class Reward(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    points_required = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# Uname - sundhark
# pswd - Will2win@1148

# uname - sundhar
# pswd - sundhar@123
