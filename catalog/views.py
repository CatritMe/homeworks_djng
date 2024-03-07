from django.shortcuts import render

from catalog.users.utils import save_user


def home(request):
    return render(request, 'catalog/home.html')

def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        save_user(name, phone, message)
    return render(request, 'catalog/contacts.html')