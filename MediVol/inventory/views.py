from django.shortcuts import render

from catalog.models import Category
from inventory.models import Box

def create(request):
    categories = Category.objects.all()
    categoryStrings = []
    
    for category in categories:
        categoryStrings.append(category.name)

    context = { 'categories': sorted(categoryStrings) }
    
    if request.session.get('initials') is not None:
        context['initials'] = request.session.get('initials')
    
    return render(request, 'inventory/create.html', context)

def box_info(request, boxid): 
    
    try: 
        #Try and get box info from the box id if exists return 
        box = Box.objects.get(box_id=boxid)
        context = { 'box': box}
        return render(request, 'inventory/box_info.html', context)
        
    except Box.DoesNotExist: 
        
        #If box does not exist in database return None 
        return render_to_response('inventory/box_not_found.html') 

