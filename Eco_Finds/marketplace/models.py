from django.db import models

# Create your models here.
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


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

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
    shipping_unit_no = models.CharField(max_length=255)
    shipping_street = models.CharField(max_length=100)
    shipping_city = models.CharField(max_length=100)
    shipping_pin = models.CharField(max_length=10)
    phone = models.CharField(max_length=15)
    payment_method = models.CharField(max_length=30)
    #created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Checkout {self.id} by {self.user.username}"

class CardDetails(models.Model):
    card_type = models.CharField(max_length=20)
    card_number = models.CharField(max_length=16)
    expiry_date = models.CharField(max_length=5)
    card_holder_name = models.CharField(max_length=100)  # Ensure this field is included
    cvv = models.CharField(max_length=3)

    def __str__(self):
        return f'Card Details for {self.card_holder_name}'

class UserRegistration(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    def check_password(self, raw_password):
        from django.contrib.auth.hashers import check_password
        return check_password(raw_password, self.password)


class Reward(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    points_required = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name




#Uname - sundhark
#pswd - Will2win@1148

#uname - sundhar
#pswd - sundhar@123