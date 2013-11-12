from django.shortcuts import render

from catalog.models import Category

def create(request):
    context = { 'categories': Category.objects.all() }
    
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

