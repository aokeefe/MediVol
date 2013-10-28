from django.utils import simplejson
from dajaxice.decorators import dajaxice_register

from catalog.models import Category, BoxName, Item

@dajaxice_register(method='GET')
def get_box_names(request, category_name):
    category = Category.objects.get(name=category_name)
    box_names = BoxName.objects.filter(letter=category)
    
    box_names_array = []
    
    for box_name in box_names:
        box_names_array.append(box_name.name)
    
    return simplejson.dumps(box_names_array)
    
@dajaxice_register(method='GET')
def get_items(request, box_name):
    box_name = BoxName.objects.get(name=box_name)
    items = Item.objects.filter(category=box_name)
    
    items_array = []
    
    for item in items:
        items_array.append(item.name)
    
    return simplejson.dumps(items_array)

@dajaxice_register
def create_box(request, initials, weight, size, items, note=''):
    items_array = []
    
    for item in items:
        items_array.append(Item.objects.get(name=item[0]))
        
    

    return simplejson.dumps(items_array)