from django.shortcuts import render

from catalog.models import Category

def create(request):
    context = { 'categories': Category.objects.all() }
    
    return render(request, 'inventory/create.html', context)