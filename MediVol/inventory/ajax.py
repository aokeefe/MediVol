from django.utils import simplejson
from dajaxice.decorators import dajaxice_register

from catalog.models import Category, BoxName, Item

@dajaxice_register(method='GET')
def get_box_names(request, category_name):
    category = Category.objects.get(name=category_name)
    box_names = BoxName.objects.filter(category=category)
    
    box_names_array = []
    
    for box_name in box_names:
        box_names_array.append(box_name.name)
    
    return simplejson.dumps(box_names_array)
    
@dajaxice_register(method='GET')
def get_items(request, box_name):
    box_name = BoxName.objects.get(name=box_name)
    items = Item.objects.filter(box_name=box_name)
    
    items_array = []
    
    for item in items:
        items_array.append(item.name)
    
    return simplejson.dumps(items_array)
    
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

@dajaxice_register
def create_box(request, initials, weight, size, items, note=''):
    new_box = Box()
    
    return simplejson.dumps(items_array)