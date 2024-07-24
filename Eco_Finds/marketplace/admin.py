from django.contrib import admin
from .models import Product, UserHistory, Review, CartItem, Order, Checkout, Cart
from .models import CardDetails, UserRegistration, Reward, Category, UserProfile
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# Unregister any already registered models to avoid conflicts
for model in [UserHistory, UserProfile]:
    if model in admin.site._registry:
        admin.site.unregister(model)

# Registering models
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(UserHistory)
admin.site.register(Review)
admin.site.register(CartItem)
admin.site.register(Cart)
admin.site.register(UserProfile)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_total_price', 'ordered_at')

admin.site.register(Checkout)
admin.site.register(CardDetails)

class UserRegistrationInline(admin.StackedInline):
    model = UserRegistration
    can_delete = False
    verbose_name_plural = 'UserRegistration'

class CustomUserAdmin(UserAdmin):
    inlines = (UserRegistrationInline,)

@admin.register(Reward)
class RewardAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'points_required', 'created_at')

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
