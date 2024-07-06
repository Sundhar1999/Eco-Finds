# marketplace/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Product
from .models import Review, Checkout, CardDetails
from .models import Order, CartItem, Reward
from .models import UserRegistration
from django.contrib.auth.hashers import make_password


#USER REGISTRATION FORM
# marketplace/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UserRegistration

class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = UserRegistration
        fields = ['username', 'email']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user



#Product Form
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image', 'category', 'carbon_emission', 'environmental_impact']


#Review Form
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']


#Order Form
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['shipping_address', 'billing_address']
        
        
#checkout form
class CheckoutForm(forms.ModelForm):
    PAYMENT_METHOD_CHOICES = [
        ('Debit Card', 'Debit Card'),
        ('Credit Card', 'Credit Card'),
    ]

    payment_method = forms.ChoiceField(
        choices=PAYMENT_METHOD_CHOICES,
        widget=forms.Select,
        required=True
    )

    class Meta:
        model = Checkout
        fields = [
            'shipping_unit_no', 'shipping_street', 'shipping_city', 'shipping_pin',
            'phone', 'payment_method'
        ]

#card details form
class CardDetailsForm(forms.ModelForm):
    class Meta:
        model = CardDetails
        fields = ['card_type', 'card_number', 'expiry_date', 'card_holder_name', 'cvv']
        widgets = {
            'card_type': forms.TextInput(attrs={'readonly': 'readonly'})
        }

#rewards
class RewardForm(forms.ModelForm):
    class Meta:
        model = Reward
        fields = ['name', 'description', 'points_required']

