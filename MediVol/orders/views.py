from django.shortcuts import render, render_to_response

from catalog.models import Category
from orders.models import Order, OrderBox
from inventory.models import Box 

#Display the main page of ordering 
def orders_main(request):
    
    categories = Category.objects.all()
    categoryStrings = []

    for category in categories:
        categoryStrings.append(category.name)

    context = { 'categories': sorted(categoryStrings) }

    return render(request, 'orders/orders.html', context)

# Display order review page
def order_review(request, orderid):

        boxes = []

        #Try and get order to review, if the order id exists return 
        order = Order.objects.get(order_number=orderid)
        
        #Try and get boxes in order 
        orderBoxes = OrderBox.objects.filter(order_for=order)
                   
        for orderBox in orderBoxes:
            box = Box.objects.get(box_id=orderBox.box)
            boxes.append(box)

        response = { 'boxes': boxes, 'order': order }
        return render(request, 'orders/review_order.html', response) 

    
        
        # I order id does not exist in database redirect to order not found page
        #return render_to_response('orders/order_not_found.html')  
