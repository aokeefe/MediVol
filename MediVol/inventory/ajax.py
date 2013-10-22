from django.utils import simplejson
from dajaxice.decorators import dajaxice_register

from catalog.models import Letter, Category, Item

@dajaxice_register(method='GET')
def get_box_names(request, category_name):
    category = Letter.objects.get(name=category_name)
    box_names = Category.objects.filter(letter=category)
    
    box_names_array = []
    
    for box_name in box_names:
        box_names_array.append(box_name.name)
    
    return simplejson.dumps(box_names_array)
    
@dajaxice_register(method='GET')
def get_items(request, box_name):
    box_name = Category.objects.get(name=box_name)
    items = Item.objects.filter(category=box_name)
    
    items_array = []
    
    for item in items:
        items_array.append(item.name)
    
    return simplejson.dumps(items_array)