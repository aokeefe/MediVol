from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
from datetime import datetime
from random import randint

from catalog.models import Category, BoxName, Item
from inventory.models import Box, Contents
from label.barcodes import BoxLabel

"""
Gets all of the box names associated with a given category.
"""
@dajaxice_register(method='GET')
def get_box_names(request, category_name):
    category = Category.objects.get(name=category_name)
    box_names = BoxName.objects.filter(category=category)
    
    box_names_array = []
    
    for box_name in box_names:
        box_names_array.append(box_name.name)
    
    return simplejson.dumps(sorted(box_names_array))

"""
Gets all of the items associated with a given box name.
"""
@dajaxice_register(method='GET')
def get_items(request, box_name):
    box_name = BoxName.objects.get(name=box_name)
    items = Item.objects.filter(box_name=box_name)
    
    items_array = []
    
    for item in items:
        items_array.append(item.name)
    
    return simplejson.dumps(sorted(items_array))

"""
Searches categories, box names, and items for a query. 
Returns the results in 'Category > Box Name > Item' form.
"""
@dajaxice_register(method='GET')
def get_search_results(request, query):
    results_array = []
    
    categories = Category.objects.filter(name__icontains=query)
    box_names = BoxName.objects.filter(name__icontains=query)
    items = Item.objects.filter(name__icontains=query)
    
    for category in categories:
        results_array.append(category.name)
    
    for box_name in box_names:
        results_array.append(box_name.category.name + ' > ' + box_name.name)
    
    for item in items:
        results_array.append(item.box_name.category.name + ' > ' + item.box_name.name + ' > ' + item.name)
    
    return simplejson.dumps(results_array)

"""
Creates a box with the given initials, weight, size, items, and note.

Item array should be of the form:
[ [item_name, item_expiration, item_quantity], [item_name, item_expiration, item_quantity] ]

That is, there is an array with arrays inside it that describe the items.
"""
@dajaxice_register
def create_box(request, initials, weight, size, items, note=''):
    # TODO: generate a real box ID
    # TODO: store note in box
    box_id = randint(100, 999)
    
    # Generates IDs until we find one that isn't in use yet
    while Box.objects.filter(box_id=box_id).exists():
        box_id = randint(100, 999)

    new_box = Box(box_id=box_id, box_size=size[:1], weight=weight, 
        entered_date=datetime.today(), initials=initials)
    
    new_box.save()
    
    request.session['initials'] = initials
    
    for item in items:
        expiration_date = item[1]
        
        if expiration_date == 'Never':
            expiration_date = None
        
        contents = Contents(box_within=new_box, 
            item=Item.objects.get(name=item[0]), 
            quantity=item[2],
            expiration=expiration_date)
        
        contents.save()
    
    return BoxLabel(new_box.barcode).get_image()