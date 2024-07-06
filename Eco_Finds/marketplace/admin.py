from django.contrib import admin
from .models import Product, UserHistory, Review, CartItem, Order, Checkout, CardDetails, UserRegistration, Reward
# Register your models here.
admin.site.register(Product)
admin.site.register(UserHistory)
admin.site.register(Review)
admin.site.register(CartItem)
admin.site.register(Checkout)
admin.site.register(CardDetails)
admin.site.register(UserRegistration)

@admin.register(Reward)
class RewardAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'points_required', 'created_at')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_price', 'ordered_at')