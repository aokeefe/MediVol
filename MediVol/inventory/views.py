from django.shortcuts import render

from catalog.models import Category

def create(request):
    context = { 'categories': Category.objects.all() }
    
    if request.session.get('initials') is not None:
        context['initials'] = request.session.get('initials')
    
    return render(request, 'inventory/create.html', context)