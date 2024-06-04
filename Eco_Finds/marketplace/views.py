from django.shortcuts import render


def home(request):
    return render(request, 'marketplace/home.html')


def login_view(request):
    return render(request, 'marketplace/Login.html')


def products(request):
    return render(request, 'marketplace/Products.html')


def register(request):
    return render(request, 'marketplace/Register.html')
