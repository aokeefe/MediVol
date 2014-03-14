from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
from datetime import datetime

from orders.models import Order, OrderBox, Customer
from orders import views as orderView
from inventory.models import Box, Contents
from catalog.models import Category, BoxName, Item
from search.Searcher import Searcher

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
    box_ids = []
    item = Item.objects.get(name=item)
    contents = Contents.objects.filter(item=item)

    for content in contents:
        box_ids.append(content.box_within.box_id)

    return simplejson.dumps(sorted(box_ids))

@dajaxice_register(method='GET')
def get_search_results(request, query):
    results_array = Searcher.search(query=query, models=[ Category, BoxName, Item, Contents ])

    try:
        box = Box.objects.get(barcode=query)
        results_array.insert(0, box.get_search_results_string())
    except Box.DoesNotExist as e:
        # shrug
        box = None

    boxes = Box.objects.filter(box_id__startswith=query)

    if len(boxes) > 0:
        for box in boxes:
            results_array.insert(0, box.get_search_results_string())

    return simplejson.dumps(results_array)

@dajaxice_register(method='GET')
def get_customer_search_results(request, query):
    return simplejson.dumps(Searcher.search(query=query, models=[ Customer ]))

@dajaxice_register(method='GET')
def get_customer_info(request, contact_name, organization_name):
    try:
        customer = Customer.objects.get(contact_name=contact_name, business_name=organization_name)
    except Customer.DoesNotExist:
        return False

    return simplejson.dumps(
        {
            'contact_email': customer.contact_email,
            'organization_address': customer.business_address,
            'shipping_address': customer.shipping_address
        }
    )

# Get Box Info
@dajaxice_register(method='GET')
def get_info(request, boxid):
    box_info = []
    box_items = []

    box = Box.objects.get(box_id=boxid)

    box_id = box.box_id

    box_size = box.box_size
    if box_size == 'S':
        box_size = 'Small'
    elif box_size == 'L':
        box_size = 'Large'

    box_weight = box.weight
    box_old_contents = box.old_contents
    box_content_ids = Contents.objects.filter(box_within=box)

    box_info.append(str(box_weight))
    box_info.append(str(box_size))
    box_info.append(str(box_id))
    box_info.append(box.get_contents_string())
    box_info.append(box.get_expiration_display())

    return simplejson.dumps(box_info)

# Registers order to database.
@dajaxice_register
def create_order(request, customer_name, customer_email, businessName, businessAddress, shipping, box_ids):
    try:
        customer = Customer.objects.get(contact_email=customer_email)
    except Customer.DoesNotExist:
        customer = Customer(contact_name=customer_name, contact_email=customer_email,
                            business_name=businessName, business_address=businessAddress,
                            shipping_address=shipping)
        customer.save()

    order_base_number = 100
    order_number_array = []

    # Calculate order number
    order_number = Order.objects.count() + order_base_number

    new_order = Order(reserved_for=customer, ship_to=customer_name, order_number=order_number, creation_date=datetime.today())
    new_order.save()

    for box_id in box_ids:
        boxOrder = Box.objects.get(box_id=box_id)
        order_box = OrderBox(order_for=new_order, box=boxOrder)
        order_box.save()

    orderNumber = Order.objects.get(order_number=order_number).order_number
    order_number_array.append(orderNumber)

    return simplejson.dumps(order_number_array)
