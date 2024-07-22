from django.contrib import admin
from .models import Product, UserHistory, Review, CartItem, Order, Checkout
from .models import CardDetails, UserRegistration, Reward, Category, UserProfile
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

# Unregister any already registered models to avoid conflicts
for model in [UserHistory, UserProfile]:
    if model in admin.site._registry:
        admin.site.unregister(model)

# Registering models
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Review)
admin.site.register(CartItem)
admin.site.register(Checkout)
admin.site.register(CardDetails)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_price', 'ordered_at')

@admin.register(Reward)
class RewardAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'points_required', 'created_at')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'visit_count', 'last_visit')
    search_fields = ('user__username',)

@admin.register(UserHistory)
class UserHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'visits', 'last_visit')
    search_fields = ('user__username',)

class UserRegistrationInline(admin.StackedInline):
    model = UserRegistration
    can_delete = False
    verbose_name_plural = 'UserRegistration'

class UserAdmin(BaseUserAdmin):
    inlines = (UserRegistrationInline,)

# Unregister the original User admin and register the new one with inlines
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
