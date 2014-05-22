from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
from datetime import datetime

from orders.models import Order, OrderBox, Customer, ShippingAddress, LockedBoxNotification
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

@dajaxice_register(method='GET')
def get_search_results(request, query, for_inventory=False):
    results_array = Searcher.search(query=query, models=[ Category, BoxName, Item, Contents, Box ], as_objects=True)
    results_strings = []

    for result in results_array:
        if isinstance(result, Contents):
            if for_inventory or not for_inventory and not result.box_within.is_locked_out():
                results_strings.append(result.get_search_results_string())
        elif isinstance(result, Box):
            if for_inventory or not for_inventory and not result.is_locked_out():
                results_strings.append(result.get_search_results_string())
        else:
            results_strings.append(result.get_search_results_string())

    try:
        box = Box.objects.get(barcode=query)

        if for_inventory or not for_inventory and not box.is_locked_out():
            results_strings.insert(0, box.get_search_results_string())
    except Box.DoesNotExist as e:
        # shrug
        box = None

    return simplejson.dumps(results_strings)

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

    box = Box.get_box(boxid)

    box_id = box.get_id()

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
def add_boxes_to_order(request, order_id, boxes={}, custom_price=False):
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return simplejson.dumps({ 'result': 0 })

    remove_all_boxes_from_order(order)

    if custom_price == '':
        custom_price = False

    for box_id, box_price in boxes.iteritems():
        if box_price != '':
            box_price = float(box_price)
        else:
            box_price = 0.00

        box_for_order = Box.get_box(box_id)

        if box_for_order.is_locked_out():
            continue

        order_box = OrderBox(order_for=order, box=box_for_order, cost=box_price)
        order_box.save()

    if custom_price is not False:
        order.price = custom_price
    else:
        order.price = None

    order.save()

    return simplejson.dumps({ 'result': 1 })

# Registers order to database.
@dajaxice_register(method='POST')
def create_order(request, order_name, customer_name, customer_email, business_name, business_address,
        new_shipping_address=None, shipping_address=None, order_id=False):
    # new_shipping_address is if they are using an address that has never
    # been used for the customer
    if new_shipping_address == '':
        new_shipping_address = None

    # shipping_address is if they are using an address that we already
    # have saved and is already associated with this customer
    if shipping_address == '':
        shipping_address = None;

    if order_id == 0:
        order_id = False

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

    if order_id is False:
        try:
            new_order = Order.objects.get(order_number=order_name)
        except Order.DoesNotExist:
            new_order = None

        if new_order is not None:
            return simplejson.dumps({ 'result': False, 'message': 'An order with this name already exists.' })

        new_order = Order(order_number=order_name, reserved_for=customer,
            ship_to=ship_to, creation_date=datetime.today())
        new_order.save()

        order = new_order
    else:
        try:
            edited_order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return simplejson.dumps({ 'result': False, 'message': 'This order does not exist.' })

        edited_order.order_number = order_name
        edited_order.reserved_for = customer
        edited_order.ship_to = ship_to
        edited_order.save()

        order = edited_order

    return simplejson.dumps({ 'result': True, 'order_number': order.id })

@dajaxice_register(method='POST')
def change_order_status(request, order_id, order_status):
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return simplejson.dumps({ 'result': 'False' })

    order.order_status = order_status
    order.save()

    return simplejson.dumps({ 'result': 'True' })

@dajaxice_register(method='POST')
def get_all_orders(request):
    orders = Order.objects.all()
    order_list = get_order_table_list_from_orders(orders)

    return simplejson.dumps(order_list)

@dajaxice_register(method='POST')
def get_all_open_orders(request):
    orders = Order.objects.exclude(order_status='F').exclude(order_status='S')
    order_list = get_order_table_list_from_orders(orders)

    return simplejson.dumps(order_list)

@dajaxice_register(method='POST')
def get_all_orders_with_status(request, status):
    orders = Order.objects.filter(order_status=status)
    order_list = get_order_table_list_from_orders(orders)

    return simplejson.dumps(order_list)

def get_order_table_list_from_orders(orders):
    order_list = []
    for order in orders:
        temp = [order.id,
                order.order_number,
                order.get_order_status_display(),
                order.reserved_for.contact_name,
                order.get_creation_date_display(),
                order.get_cost(),
                order.get_weight()]
        order_list.append(temp)
    return order_list

@dajaxice_register(method='POST')
def delete_order(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return simplejson.dumps({ 'result': False })

    order_boxes = OrderBox.objects.filter(order_for=order)

    for order_box in order_boxes:
        order_box.delete()

    order.delete()

    return simplejson.dumps({ 'result': True })

@dajaxice_register(method='POST')
def delete_locked_box_notifications(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return simplejson.dumps({ 'result': False, 'message': 'This order does not exist.' })

    locked_box_notifications = LockedBoxNotification.objects.filter(removed_from_order=order)

    for locked_box_notification in locked_box_notifications:
        locked_box_notification.delete()

    return simplejson.dumps({ 'result': True })

@dajaxice_register(method='POST')
def get_order_packing_list(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return simplejson.dumps({ 'result': 'False' })
    csv = []
    header = '"Order Name","Box Name","Contents","Weight","Expiration Date"'
    csv.append(header)

    orderBoxs = OrderBox.objects.filter(order_for=order)

    for orderBox in orderBoxs:
        temp = (get_csv_string(order.order_number) + ',' +
                get_csv_string(orderBox.box.get_most_populous_box_name()) + ',' +
                get_csv_string(orderBox.box.get_contents_string()) + ',' +
                get_csv_string(orderBox.box.weight) + ',' +
                get_csv_string(orderBox.box.get_expiration_display()))

        csv.append(temp)

    return simplejson.dumps(csv)

def get_csv_string(value):
    return '"' + str(value).replace('"', '""') + '"'
