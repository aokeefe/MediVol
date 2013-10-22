from django.shortcuts import render

from catalog.models import Letter

def create(request):
    if request.method == 'POST':
        context = {}
    else:
        context = {}
        
    context['categories'] = Letter.objects.all()
    
    return render(request, 'inventory/create.html', context)