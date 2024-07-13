# marketplace/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Product
from .models import Review, Checkout, CardDetails
from .models import Order, CartItem, Reward
from .models import UserRegistration
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import AuthenticationForm



#USER REGISTRATION FORM
# marketplace/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UserRegistration

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
        }
       
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error('password2', "Passwords do not match.")

        return cleaned_data

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
        fields = ['card_type', 'card_number', 'expiry_date', 'cardholder_name', 'cvv']
        widgets = {
            'card_type': forms.TextInput(attrs={'readonly': 'readonly'})
        }

#rewards
class RewardForm(forms.ModelForm):
    class Meta:
        model = Reward
        fields = ['name', 'description', 'points_required']