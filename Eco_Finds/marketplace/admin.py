from django.contrib import admin
from .models import Product, UserHistory, Review, CartItem, Order, Checkout, CardDetails, UserRegistration, Reward
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# Register your models here.
admin.site.register(Product)
admin.site.register(UserHistory)
admin.site.register(Review)
admin.site.register(CartItem)
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_price', 'ordered_at')
admin.site.register(Checkout)
admin.site.register(CardDetails)
class UserRegistrationInline(admin.StackedInline):
    model = UserRegistration
    can_delete = False
    verbose_name_plural = 'UserRegistration'

class UserAdmin(UserAdmin):
    inlines = (UserRegistrationInline,)

@admin.register(Reward)
class RewardAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'points_required', 'created_at')


admin.site.unregister(User)
admin.site.register(User, UserAdmin)

