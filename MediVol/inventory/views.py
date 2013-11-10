from django.shortcuts import render

from catalog.models import Category

def create(request):
    context = { 'categories': Category.objects.all() }
    
    return render(request, 'inventory/create.html', context)

def box_inf(request, boxid): 
    
    try: 
        #Try and get box info from the box id if exists return 
        box = Box.objects.get(box_id=boxid)
    except Box.DoesNotExist: 
        
        #If box does not exist in database return None 
        box = None 

    if (box == None): 
        return render_to_response('inventory/box_not_found.html') 
    else:
        context = { 'box': box} 
        return render(request, 'inventory/box_info.html', context)

