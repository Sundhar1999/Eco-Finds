from django.contrib import admin

from .models import Product, UserHistory, Review, CartItem, Order

# Register your models here.
admin.site.register(Product)
admin.site.register(UserHistory)
admin.site.register(Review)
admin.site.register(CartItem)
admin.site.register(Order)