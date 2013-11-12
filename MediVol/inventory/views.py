from django.shortcuts import render

from catalog.models import Category

def create(request):
    categories = Category.objects.all()
    categoryStrings = []
    
    for category in categories:
        categoryStrings.append(category.name)

    context = { 'categories': sorted(categoryStrings) }
    
    if request.session.get('initials') is not None:
        context['initials'] = request.session.get('initials')
    
    return render(request, 'inventory/create.html', context)