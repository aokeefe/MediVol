from django.shortcuts import render, render_to_response

from catalog.models import Category
from orders.models import Order, OrderBox
from inventory.models import Box

def orders_home(request):
    context = { 'orders': Order.objects.all() }

    return render(request, 'orders/orders.html', context)

#Display the create page of ordering
def create_order(request, order_id=0):
    categories = Category.objects.all()
    categoryStrings = []
    order = False
    num_addresses = 0
    num_boxes = 0
    total_price = 0.00
    custom_price = 0.00

    if order_id != 0:
        try:
            order = Order.objects.get(order_number=order_id)
            num_addresses = len(order.reserved_for.shippingaddress_set.all())
            num_boxes = len(order.orderbox_set.all())

            for orderbox in order.orderbox_set.all():
                total_price = total_price + orderbox.cost

            custom_price = order.price
        except Order.DoesNotExist:
            order_id = 0

    for category in categories:
        categoryStrings.append(category.name)

    context = {
        'categories': sorted(categoryStrings),
        'order_id': order_id,
        'order': order,
        'num_address': num_addresses,
        'num_boxes': num_boxes,
        'total_price': '%.2f' % total_price,
        'custom_price': '%.2f' % custom_price
    }

    return render(request, 'orders/create_order.html', context)

# Display order review page
def order_review(request, orderid):

  try:
        boxes = []
        boxOrderBoxPair = []

        #Try and get order to review, if the order id exists return
        order = Order.objects.get(order_number=orderid)

        #Try and get boxes in order
        orderBoxes = OrderBox.objects.filter(order_for=order)

        for orderBox in orderBoxes:
            box = Box.objects.get(box_id=orderBox.box)

            boxOrderBoxPair.append(box)
            boxOrderBoxPair.append(orderBox)

            boxes.append(boxOrderBoxPair)

        response = { 'boxes': boxes, 'order': order}
        return render(request, 'orders/review_order.html', response)

  except:
        # If order id does not exist in database redirect to order not found page
        return render_to_response('orders/order_not_found.html')
