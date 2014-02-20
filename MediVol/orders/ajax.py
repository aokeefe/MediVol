from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
from datetime import datetime

from orders.models import Order, OrderBox
from orders import views as orderView
from inventory.models import Box, Contents
from catalog.models import Category, BoxName, Item

# Gets all of the box names associated with a given category
@dajaxice_register(method='GET')
def get_box_names(request, category_name):
    box_names = Category.objects.get(name=category_name).boxname_set.all()

    box_names_array = []

    for box_name in box_names:
        box_names_array.append(box_name.name)

    return simplejson.dumps(sorted(box_names_array))

# Gets all of the items associated with a given box name.
@dajaxice_register(method='GET')
def get_items(request, box_name):
    items = BoxName.objects.get(name=box_name).item_set.all()

    items_array = []

    for item in items:
        items_array.append(item.name)

    return simplejson.dumps(sorted(items_array))

# Gets all boxes associated with items
@dajaxice_register(method='GET')
def get_box_ids(request, item):
    
    boxs_ids = []
    item = Item.objects.get(name=item)
    contents = Contents.objects.filter(item=item)

    for content in contents:
        boxs_ids.append(content.box_within.box_id)
    
    return simplejson.dumps(sorted(boxs_ids))

# Search box ids
@dajaxice_register(method='GET')
def get_search_results(request, query):

    results_array = []
    contents = []

    categories = Category.objects.filter(name__icontains=query)
    box_names = BoxName.objects.filter(name__icontains=query)
    items = Item.objects.filter(name__icontains=query)

    for category in categories:
        results_array.append(category.name)

    for box_name in box_names:
        results_array.append(box_name.category.name + ' > ' + box_name.name)

    for item in items:
        results_array.append(item.box_name.category.name + ' > ' + item.box_name.name + ' > '+ item.name)
        contents.append(Contents.objects.filter(item=item))
 
    for content in contents:
        results_array.append(content.item.box_name.category.name + ' > ' + content.item.box_name.name + ' > ' + content.item.name + ' > ' + content.box_within.box_id)

    return simplejson.dumps(results_array)

# Get Box Info 
@dajaxice_register(method='GET')
def get_info(request, boxid):

    box_info = []
    box_items = []
    box = Box.objects.get(box_id=boxid)
    box_id = box.box_id
    box_info.append(str(box_id))
    box_size = box.box_size
    box_info.append(str(box_size))
    box_weight = box.weight
    box_info.append(str(box_weight))
    box_old_contents = box.old_contents
    box_new_content_ids = Contents.objects.get(box_within=box)

    return simplejson.dumps(box_info)

# Registers order to database.
@dajaxice_register
def create_order(request, ship_to, reserved_for, box_ids):

    order_base_number = 100
    order_number_array = []

    # Calculate order number
    order_number = Order.objects.count() + order_base_number

    new_order = Order(reserved_for=reserved_for, ship_to=ship_to, order_number=order_number, creation_date=datetime.today())
    new_order.save()

    for box_id in box_ids:
        boxOrder = Box.objects.get(box_id=box_id)
        order_box = OrderBox(order_for=new_order, box=boxOrder)
        order_box.save()

    orderNumber = Order.objects.get(order_number=order_number).order_number
    order_number_array.append(orderNumber)    

    return simplejson.dumps(order_number_array)
