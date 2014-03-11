from django.shortcuts import render

from catalog.models import Category
from inventory.models import Box, Contents
from orders.models import Order, OrderBox

def create(request):
    categories = Category.objects.all()
    categoryStrings = []
    
    for category in categories:
        categoryStrings.append(category.name)
    
    context = { 'categories': sorted(categoryStrings) }
    
    return render(request, 'inventory/create.html', context)

def box_info(request, boxid): 
    
    try: 
        #Try and get box info from the box id if exists return 
        box = Box.objects.get(box_id=boxid)
        box_contents = []
    
        if box.old_contents is None: 
          
            box_contents = Contents.objects.filter(box_within=box)

        else: 
      
            box_contents = box.old_contents    
 
        # Search if box is related to orders.
        try:

            order_box = OrderBox.objects.get(box=box)
            order_number = Order.objects.get(order).order_number

        except OrderBox.DoesNotExist:

            order_number = None

        context = { 'box': box, 'box_contents': box_contents, 'order_number': order_number }
        return render(request, 'inventory/box_info.html', context)
        
    except Box.DoesNotExist: 
        
        #If box does not exist in database redirect to box not found page
        return render_to_response('inventory/box_not_found.html') 

def barcode_box_info(request, barcodeid):
    
    try:
        
        #Try and get the box info from the box id if exists return 
        box = Box.objects.get(barcode=barcodeid)
        box_contents = []

        if box.old_contents is None:

            box_contentss = Contents.objects.filter(box_within=box)

        else:

            box_contents = box.old_contents

        # Search if box is related to orders.
        try:

            order_box = OrderBox.objects.get(box=box)
            order_number = Order.objects.get(order).order_number

        except OrderBox.DoesNotExist:

            order_number = None

        context = { 'box': box, 'box_contents': box_contents, 'order_number': order_number }
        return render(request, 'inventory/box_info.html', context)

    except Box.DoesNotExist:

        #If box does not exist in databse redirect to box not found page
        return render_to_response('inventory/box_not_found.html')
