from django.shortcuts import render, render_to_response
from django.contrib.auth.decorators import login_required, user_passes_test
from administration.UserTests import UserTests

from catalog.models import Category
from orders.models import Order, OrderBox, LockedBoxNotification
from inventory.models import Box

@login_required(login_url='/login/')
@user_passes_test(UserTests.user_is_admin, login_url='/administration/forbidden')
def orders_home(request):
    choices = Order._meta.get_field('order_status').choices
    orders = Order.objects.exclude(order_status='F').exclude(order_status='S')
    context = { 'orders': orders, 'statuses': choices}

    return render(request, 'orders/orders.html', context)

@login_required(login_url='/login/')
@user_passes_test(UserTests.user_is_admin, login_url='/administration/forbidden')
#Display the create page of ordering
def create_order(request, order_id=0, step_num=1, box_to_add='0'):
    step_num = int(step_num)
    categories = Category.objects.all()
    categoryStrings = []
    order = False
    num_addresses = 0
    num_boxes = 0
    total_price = 0.00
    custom_price = 0.00

    if order_id != 0:
        try:
            order = Order.objects.get(id=order_id)
            num_addresses = len(order.reserved_for.shippingaddress_set.all())
            num_boxes = len(order.orderbox_set.all())

            for order_box in order.orderbox_set.all():
                total_price = total_price + order_box.cost

            custom_price = order.price
        except Order.DoesNotExist:
            order_id = 0

    for category in categories:
        categoryStrings.append(category.name)

    if total_price is None:
        total_price = 0.00

    if custom_price is None:
        custom_price = 0.00

    box = None

    if box_to_add != '0':
        box = Box.get_box(box_to_add)

    context = {
        'categories': sorted(categoryStrings),
        'order_id': order_id,
        'order': order,
        'num_addresses': num_addresses,
        'num_boxes': num_boxes,
        'total_price': '%.2f' % total_price,
        'custom_price': '%.2f' % custom_price,
        'step_num': step_num,
        'box_to_add': box
    }

    return render(request, 'orders/create_order.html', context)

@login_required(login_url='/login/')
@user_passes_test(UserTests.user_is_admin, login_url='/administration/forbidden')
# Display order review page
def order_review(request, orderid):
    try:
        #Try and get order to review, if the order id exists return
        order = Order.objects.get(id=orderid)
    except:
        try:
            order = Order.objects.get(order_number=orderid)
        except Order.DoesNotExist:
            # If order id does not exist in database redirect to order not found page
            return render_to_response('orders/order_not_found.html')

    boxes = []
    box_orderbox_pair = []
    locked_boxes = LockedBoxNotification.objects.filter(removed_from_order=order)

    if locked_boxes.count() == 0:
        locked_boxes = None
    else:
        locked_box_strings = []

        for locked_box in locked_boxes:
            locked_box_strings.append(locked_box.box.get_url())

        locked_boxes = ', '.join(locked_box_strings)

    response = {
        'order_boxes': OrderBox.objects.filter(order_for=order),
        'order': order,
        'order_statuses': Order.ORDER_STATUS,
        'locked_boxes': locked_boxes
    }

    return render(request, 'orders/review_order.html', response)
