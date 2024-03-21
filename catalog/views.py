from django.shortcuts import render

from catalog.models import Product
from catalog.users.utils import save_user


def home(request):
    products_list = Product.objects.all()
    context = {
        'object_list': products_list,
        'title': 'Главная'
    }
    return render(request, 'catalog/home.html', context)

def contacts(request):
    context = {
        'title': 'Контакты'
    }
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        save_user(name, phone, message)
    return render(request, 'catalog/contacts.html', context)

def products(request, pk):
    prod = Product.objects.get(pk=pk)
    context = {
        'object_list': Product.objects.filter(pk=pk),
        'title': f'Информация о {prod.title}'
    }
    return render(request, 'catalog/products.html', context)