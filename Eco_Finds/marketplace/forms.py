from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Product
from .models import Checkout, CardDetails, Reward
from .models import Order, CartItem
from .models import UserRegistration
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
import re



#USER REGISTRATION FORM
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    profile_picture = forms.ImageField(label='Profile Picture', required=False)
    security_question1 = forms.CharField(label='Security Question 1')
    security_answer1 = forms.CharField(label='Answer 1')
    security_question2 = forms.CharField(label='Security Question 2')
    security_answer2 = forms.CharField(label='Answer 2')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'profile_picture', 'security_question1', 'security_answer1', 'security_question2', 'security_answer2']
        labels = {
            'password1': 'Password',
            'password2': 'Confirm Password',
        }
        widgets = {
            'password1': forms.PasswordInput(attrs={'placeholder': 'Password'}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),
        }
        help_texts = {
            'username': None,
            'password1': None,
            'password2': None,
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists.")
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise forms.ValidationError("Invalid email format.")
        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        errors = []

        if len(password1) < 8:
            errors.append("Your password must contain at least 8 characters.")
        if not any(char.isdigit() for char in password1):
            errors.append("Your password must contain at least one digit.")
        if not any(char.isalpha() for char in password1):
            errors.append("Your password must contain at least one letter.")
        if re.search(r'(.)\1{2,}', password1):
            errors.append("Your password can't contain three repeating characters in a row.")
        if User.objects.filter(username=password1).exists():
            errors.append("Your password can't be too similar to your username.")
        if re.search(r'^[a-zA-Z]+$', password1):
            errors.append("Your password can't be entirely alphabetic.")

        if errors:
            raise forms.ValidationError(errors)

        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")

        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            user_registration, created = UserRegistration.objects.get_or_create(
                user=user,
                defaults={
                    'profile_picture': self.cleaned_data['profile_picture'],
                    'security_question1': self.cleaned_data['security_question1'],
                    'security_answer1': self.cleaned_data['security_answer1'],
                    'security_question2': self.cleaned_data['security_question2'],
                    'security_answer2': self.cleaned_data['security_answer2']
                }
            )
            if not created:
                user_registration.profile_picture = self.cleaned_data['profile_picture']
                user_registration.security_question1 = self.cleaned_data['security_question1']
                user_registration.security_answer1 = self.cleaned_data['security_answer1']
                user_registration.security_question2 = self.cleaned_data['security_question2']
                user_registration.security_answer2 = self.cleaned_data['security_answer2']
                user_registration.save()
        return user

class ForgetPasswordForm(forms.Form):
    username = forms.CharField(max_length=150)
    

class SetNewPasswordForm(forms.Form):
    username = forms.CharField(widget=forms.HiddenInput())
    new_password = forms.CharField(label='New Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(label='Confirm New Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data



#Product Form
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image', 'category', 'carbon_emission', 'environmental_impact']



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

        widgets = {
            'shipping_unit_no': forms.TextInput(attrs={'placeholder': 'Shipping Unit No'}),
            'shipping_street': forms.TextInput(attrs={'placeholder': 'Shipping Street Address'}),
            'shipping_city': forms.TextInput(attrs={'placeholder': 'Shipping City'}),
            'shipping_pin': forms.TextInput(attrs={'placeholder': 'A1B2C3'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Phone Number'}),
        }
        help_texts = {
            'shipping_pin': 'Enter the PIN in the format A1B2C3.',
            'phone': 'Enter a 10-digit phone number.',
        }

    def clean_shipping_pin(self):
        shipping_pin = self.cleaned_data.get('shipping_pin')
        if not re.match(r'^[A-Za-z]{1}\d{1}[A-Za-z]{1}\d{1}[A-Za-z]{1}\d{1}$', shipping_pin):
            raise forms.ValidationError("Invalid PIN code. It should be in the format A1B2C3.")
        return shipping_pin

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not re.match(r'^\d{10}$', phone):
            raise forms.ValidationError("Invalid phone number. It should be 10 digits.")
        return phone

class CardDetailsForm(forms.ModelForm):
    class Meta:
        model = CardDetails
        fields = ['card_type', 'card_number', 'expiry_date', 'cardholder_name', 'cvv']
        widgets = {
            'card_type': forms.TextInput(attrs={'readonly': 'readonly', 'placeholder': 'Card Type'}),
            'card_number': forms.TextInput(attrs={'placeholder': 'Card Number'}),
            'expiry_date': forms.TextInput(attrs={'placeholder': 'MM/YY'}),
            'cardholder_name': forms.TextInput(attrs={'placeholder': 'Cardholder Name'}),
            'cvv': forms.TextInput(attrs={'placeholder': 'CVV'}),
        }

    def clean_card_number(self):
        card_number = self.cleaned_data.get('card_number')
        if not re.match(r'^\d{16}$', card_number):
            raise forms.ValidationError("Invalid card number. It should be 16 digits.")
        return card_number

    def clean_expiry_date(self):
        expiry_date = self.cleaned_data.get('expiry_date')
        if not re.match(r'^\d{2}/\d{2}$', expiry_date):
            raise forms.ValidationError("Invalid expiry date format. Use MM/YY.")
        return expiry_date

    def clean_cvv(self):
        cvv = self.cleaned_data.get('cvv')
        if not re.match(r'^\d{3}$', cvv):
            raise forms.ValidationError("Invalid CVV. It should be 3 digits.")
        return cvv

class RewardForm(forms.ModelForm):
    class Meta:
        model = Reward
        fields = ['name', 'description', 'points_required']