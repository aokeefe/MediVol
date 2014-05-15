from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from administration.UserTests import UserTests

from catalog.models import Category
from inventory.models import Box, Contents, Warehouse
from orders.models import Order, OrderBox

@login_required(login_url='/login/')
@user_passes_test(UserTests.user_can_create_box, login_url='/administration/forbidden')
def create(request, order_id=0):
    categories = Category.objects.all()
    categoryStrings = []

    for category in categories:
        categoryStrings.append(category.name)

    order = False

    if order_id != 0:
        order = Order.objects.get(id=order_id)

    context = {
        'categories': sorted(categoryStrings),
        'order_id': order_id,
        'order': order,
        'warehouses': Warehouse.objects.all(),
        'box': None
    }

    return render(request, 'inventory/create.html', context)

@login_required(login_url='/login/')
@user_passes_test(UserTests.user_can_create_box, login_url='/administration/forbidden')
def edit(request, box_id):
    box = Box.get_box(box_id)

    if box is None:
        return render(request, 'inventory/box_not_found.html')

    categories = Category.objects.all()
    categoryStrings = []

    for category in categories:
        categoryStrings.append(category.name)

    context = {
        'categories': sorted(categoryStrings),
        'order_id': 0,
        'warehouses': Warehouse.objects.all(),
        'box': box
    }

    return render(request, 'inventory/create.html', context)

@login_required(login_url='/login')
@user_passes_test(UserTests.user_can_see_box_info, login_url='/administration/forbidden')
def box_info(request, boxid):
    #Try and get box info from the box id if exists return
    box = Box.get_box(boxid)

    if box is None:
        return render(request, 'inventory/box_not_found.html')

    box_contents = []

    if box.old_contents is None:
        box_contents = Contents.objects.filter(box_within=box)
    else:
        box_contents = box.old_contents

    # Search if box is related to orders.
    try:
        order = OrderBox.objects.get(box=box).order_for
    except OrderBox.DoesNotExist:
        order = None

    context = {
        'box': box,
        'box_contents': box_contents,
        'order': order,
        'warehouses': Warehouse.objects.all()
    }

    return render(request, 'inventory/box_info.html', context)

@login_required(login_url='/login/')
@user_passes_test(UserTests.user_can_see_box_info, login_url='/administration/forbidden')
def barcode_box_info(request, barcodeid):
    try:
        #Try and get the box info from the box id if exists return
        box = Box.objects.get(barcode=barcodeid)
        box_contents = []

        if box.old_contents is None:
            box_contentss = Contents.objects.filter(box_within=box)
        else:
            box_contents = box.old_contents

        # Search if box is related to orders.
        try:
            order_box = OrderBox.objects.get(box=box)
            order_number = Order.objects.get(order).order_number
        except OrderBox.DoesNotExist:
            order_number = None

        context = { 'box': box, 'box_contents': box_contents, 'order_number': order_number }

        return render(request, 'inventory/box_info.html', context)
    except Box.DoesNotExist:
        #If box does not exist in databse redirect to box not found page
        return render_to_response('inventory/box_not_found.html')

@login_required(login_url='/login/')
@user_passes_test(UserTests.user_can_see_inventory, login_url='/administration/forbidden')
def inventory_view(request):
    categories = Category.objects.all()
    categoryStrings = []

    for category in categories:
        categoryStrings.append(category.name)

    context = { 'categories': sorted(categoryStrings) }

    return render(request, 'inventory/inventory.html', context)

@login_required(login_url='/login/')
@user_passes_test(UserTests.user_can_transfer_boxes, login_url='/administration/forbidden')
def box_transfer(request):
    context = { 'warehouses': Warehouse.objects.all() }

    return render(request, 'inventory/box_transfer.html', context)
