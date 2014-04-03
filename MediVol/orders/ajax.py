from django.utils import simplejson
from itertools import chain
from dajaxice.decorators import dajaxice_register
from datetime import datetime

from orders.models import Order, OrderBox, Customer, ShippingAddress
from orders import views as orderView
from inventory.models import Box, Contents
from catalog.models import Category, BoxName, Item
from search.Searcher import Searcher

ORDER_BASE_NUMBER = 100

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
        box_ids.append(content.box_within.get_id())

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

    query = '%%%s%%' % query

    boxes = chain(Box.objects.filter(box_id__istartswith=query),
        Box.objects.raw(
            '''SELECT * FROM inventory_box
            INNER JOIN catalog_category ON inventory_box.box_category_id = catalog_category.id
            WHERE CONCAT(catalog_category.letter, inventory_box.box_id) LIKE %s''',
            [query]
        )
    )

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

    addresses = []

    for shipping_address in customer.shippingaddress_set.all():
        addresses.append(shipping_address.address)

    return simplejson.dumps(
        {
            'contact_email': customer.contact_email,
            'organization_address': customer.business_address,
            'shipping_addresses': addresses
        }
    )

# Get Box Info
@dajaxice_register(method='GET')
def get_info(request, boxid):
    box_info = []
    box_items = []

    try:
        box = Box.objects.get(box_id=boxid)
    except Box.DoesNotExist:
        boxes = Box.objects.raw(
            '''SELECT * FROM inventory_box
            INNER JOIN catalog_category ON inventory_box.box_category_id = catalog_category.id
            WHERE CONCAT(catalog_category.letter, inventory_box.box_id) = %s''',
            [boxid]
        )

        for box_found in boxes:
            box = Box.objects.get(box_id=box_found.box_id)
            break

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

def remove_all_boxes_from_order(order):
    order_boxes = order.orderbox_set.all()

    for order_box in order_boxes:
        order_box.delete()

@dajaxice_register(method='POST')
def add_boxes_to_order(request, order_number, boxes={}, custom_price=False):
    try:
        order = Order.objects.get(order_number=order_number)
    except Order.DoesNotExist:
        return simplejson.dumps({ 'result': 0 })

    remove_all_boxes_from_order(order)

    if custom_price == '':
        custom_price = False

    order_price = 0

    for box_id, box_price in boxes.iteritems():
        box_id = int(box_id)

        if box_price != '':
            box_price = float(box_price)
        else:
            box_price = 0.00

        box_for_order = Box.objects.get(box_id=box_id)

        order_box = OrderBox(order_for=order, box=box_for_order, cost=box_price)
        order_box.save()

        order_price = order_price + box_price

    if custom_price is not False:
        order.price = custom_price
    else:
        order.price = order_price

    order.save()

    return simplejson.dumps({ 'result': 1 })

# Registers order to database.
@dajaxice_register(method='POST')
def create_order(request, customer_name, customer_email, business_name, business_address,
        new_shipping_address=None, shipping_address=None, order_number=0):
    # new_shipping_address is if they are using an address that has never
    # been used for the customer
    if new_shipping_address == '':
        new_shipping_address = None

    # shipping_address is if they are using an address that we already
    # have saved and is already associated with this customer
    if shipping_address == '':
        shipping_address = None;

    try:
        customer = Customer.objects.get(contact_name=customer_name, business_name=business_name)

        customer.contact_email = customer_email
        customer.business_address = business_address
    except Customer.DoesNotExist:
        customer = Customer(contact_name=customer_name, contact_email=customer_email,
                            business_name=business_name, business_address=business_address)

    customer.save()

    ship_to = None

    if new_shipping_address is not None:
        try:
            ship_to = ShippingAddress.objects.get(customer=customer, address=new_shipping_address)
        except ShippingAddress.DoesNotExist:
            ship_to = ShippingAddress(customer=customer, address=new_shipping_address)
            ship_to.save()
    elif shipping_address is not None:
        try:
            ship_to = ShippingAddress.objects.get(customer=customer, address=shipping_address)
        except ShippingAddress.DoesNotExist:
            ship_to = ShippingAddress(customer=customer, address=shipping_address)
            ship_to.save()

    if order_number == 0:
        # Calculate order number
        order_number = len(Order.objects.all()) + ORDER_BASE_NUMBER

        new_order = Order(reserved_for=customer, ship_to=ship_to, order_number=order_number, creation_date=datetime.today())
        new_order.save()
    else:
        try:
            edited_order = Order.objects.get(order_number=order_number)
        except Order.DoesNotExist:
            return simplejson.dumps({ 'order_number': 0 })

        edited_order.reserved_for = customer
        edited_order.ship_to = ship_to
        edited_order.save()

    return simplejson.dumps({ 'order_number': order_number })
