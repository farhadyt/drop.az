# catalog/views.py
from django.shortcuts import render
from .models import Product # Product modelini import edirik

def home(request):
    # Yalnız satışda olan məhsulları götürürük
    products = Product.objects.filter(available=True)
    
    # Məhsulları template-ə göndərmək üçün 'context' adlı bir lüğət yaradırıq
    context = {
        'products': products
    }
    return render(request, 'catalog/home.html', context)