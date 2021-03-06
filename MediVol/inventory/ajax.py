from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
from datetime import datetime
from random import randint
from HTMLParser import HTMLParser

from catalog.models import Category, BoxName, Item
from inventory.models import Box, Contents, Warehouse
from label.barcodes import BoxLabel
from orders.models import OrderBox, Order

from haystack.query import SearchQuerySet

from search.Searcher import Searcher

"""
Gets all of the box names associated with a given category.
"""
@dajaxice_register(method='GET')
def get_box_names(request, category_name):
    return simplejson.dumps(Searcher.get_box_names(category_name))

"""
Gets all of the items associated with a given box name.
"""
@dajaxice_register(method='GET')
def get_items(request, box_name):
    return simplejson.dumps(Searcher.get_items(box_name))

"""
Searches categories, box names, and items for a query.
Returns the results in 'Category > Box Name > Item' form.
"""
@dajaxice_register(method='GET')
def get_search_results(request, query):
    return simplejson.dumps(Searcher.search(query=query, models=[ Category, BoxName, Item ]))

"""
Creates a box with the given initials, weight, size, items, and note.

Item array should be of the form:
[ [item_name, item_expiration, item_quantity], [item_name, item_expiration, item_quantity] ]

That is, there is an array with arrays inside it that describe the items.
"""
@dajaxice_register(method='POST')
def create_box(request, initials, weight, size, items, warehouse_abbrev, note='', box_id=None, category=None):
    htmlParser = HTMLParser()

    initials = htmlParser.unescape(initials)
    warehouse_abbrev = htmlParser.unescape(warehouse_abbrev)
    note = htmlParser.unescape(note)

    try:
        warehouse = Warehouse.objects.get(abbreviation=warehouse_abbrev)
    except Warehouse.DoesNotExist:
        return simplejson.dumps({'result': 'False'})

    if note == '':
        note = None

    if category == '':
        category = None
    else:
        try:
            category = Category.objects.get(name=category)
        except Category.DoesNotExist:
            return simplejson.dumps({'result': 'False'})

    if box_id is None or box_id == 0:
        new_box = Box(box_size=size[:1], weight=weight,
            entered_date=datetime.today(), initials=initials.upper(), warehouse=warehouse, note=note)

        if category is not None:
            new_box.box_category = category

        new_box.save()

        box = new_box;
    else:
        box = Box.get_box(box_id)

        if box is None:
            return simplejson.dumps({'result': 'False'})

        box.box_size = size[:1]
        box.weight = weight
        box.initials = initials.upper()
        box.warehouse = warehouse
        box.note = note

        if category is not None:
            box.box_category = category

        box.save()

        for content in box.contents_set.all():
            content.delete()

    for item_info in items:
        # convert HTML entities in item name (e.g. &amp;)
        item_info[0] = htmlParser.unescape(item_info[0])

        # convert HTML entities in box name
        item_info[3] = htmlParser.unescape(item_info[3])

        expiration_date = item_info[1]

        if expiration_date == 'Never':
            expiration_date = None

        contents = Contents(box_within=box,
            item=Item.objects.get(name=item_info[0], box_name=BoxName.objects.get(name=item_info[3])),
            quantity=item_info[2],
            expiration=expiration_date)

        contents.save()

    return simplejson.dumps(
        {
            'result': 'True',
            'label': request.build_absolute_uri('/label/create/' + box.barcode),
            'box_id': box.get_id()
        }
    )

@dajaxice_register(method='POST')
def get_label(request, box_id):
    box = Box.get_box(box_id)
    return request.build_absolute_uri('/label/create/' + box.barcode)

def box_to_object(box):
    try:
        warehouse = box.warehouse.abbreviation
    except AttributeError:
        warehouse = ''

    order_boxes = OrderBox.objects.filter(box=box)
    orders = []

    for order_box in order_boxes:
        orders.append(order_box.order_for.order_number)

    return {
        'id': box.get_id(),
        'size': box.get_box_size_display(),
        'weight': str(box.weight) + ' lbs',
        'contents': box.get_contents_string(),
        'expiration': box.get_expiration_display(),
        'warehouse': warehouse,
        'orders': orders,
        'old_box': box.old_box_flag
    }

@dajaxice_register(method='GET')
def get_boxes_with_item(request, item_name, box_name, for_order_page=False):
    box = BoxName.objects.get(name=box_name)
    item = Item.objects.get(name=item_name, box_name=box)
    box_list = []
    boxes = []
    contents = Contents.objects.filter(item=item)

    for content in contents:
        if content.box_within.box_id not in boxes:
            box = content.box_within

            if not for_order_page or for_order_page and not box.is_locked_out():
                boxes.append(box.box_id)
                box_list.append(box_to_object(box))

    return simplejson.dumps(box_list)

@dajaxice_register(method='POST')
def get_boxes_with_box_name(request, box_name, for_order_page=False):
    box_name = BoxName.objects.get(name=box_name)
    items = Item.objects.filter(box_name=box_name)
    contents = Contents.objects.filter(item__in=items)
    boxes = []
    box_list = []

    for content in contents:
        if content.box_within.box_id not in boxes:
            box = content.box_within

            if not for_order_page or for_order_page and not box.is_locked_out():
                boxes.append(box.box_id)
                box_list.append(box_to_object(box))

    return simplejson.dumps(box_list)

@dajaxice_register(method='POST')
def get_boxes_with_category(request, category_name, for_order_page=False):
    category = Category.objects.get(name=category_name)
    boxes = Box.objects.filter(box_category=category)

    box_list = []

    for box in boxes:
        if not for_order_page or for_order_page and not box.is_locked_out():
            box_list.append(box_to_object(box))

    return simplejson.dumps(box_list)

@dajaxice_register(method='GET')
def get_box_by_id(request, box_id):
    box = Box.get_box(box_id)

    return simplejson.dumps(box_to_object(box))

@dajaxice_register(method='GET')
def get_box_by_barcode(request, barcode):
    try:
        box = Box.objects.get(barcode=barcode)
    except Box.DoesNotExist:
        return simplejson.dumps({ 'result': False, 'barcode': barcode })

    return simplejson.dumps(
        {
            'result': True,
            'box_id': box.get_id(),
            'warehouse': box.warehouse.name,
            'weight': '%.1f' % box.weight,
            'size': box.get_box_size_display(),
            'expiration': box.get_expiration_display()
        }
    )

@dajaxice_register(method='GET')
def get_warehouse_abbreviations(request):
    abbreviations = []
    warehouses = Warehouse.objects.all()
    for warehouse in warehouses:
        abbreviations.append(warehouse.abbreviation)
    return simplejson.dumps(abbreviations)

@dajaxice_register(method='POST')
def set_warehouse(request, box_id, warehouse_abbreviation):
    if request.user.groups.all()[0].name != 'Admin' or request.user.groups.all()[0].name != 'Box Transfer':
        return simplejson.dumps({'message': 'False'})

    try:
        warehouse = Warehouse.objects.get(abbreviation=warehouse_abbreviation)
    except Warehouse.DoesNotExist:
        return simplejson.dumps({'message': 'False'})

    box = Box.get_box(box_id)

    if box is None:
        return simplejson.dumps({'message': 'False'})

    box.warehouse = warehouse
    box.save();
    return simplejson.dumps({'message': 'True'})

@dajaxice_register(method='POST')
def transfer_boxes(request, boxes, warehouse_abbreviation):
    try:
        warehouse = Warehouse.objects.get(abbreviation=warehouse_abbreviation)
    except Warehouse.DoesNotExist:
        return simplejson.dumps({ 'result': False })

    for box_id in boxes:
        box = Box.get_box(box_id)

        if box is not None:
            box.warehouse = warehouse
            box.save()

    return simplejson.dumps({ 'result': True })

@dajaxice_register(method='POST')
def delete_box(request, box_id):
    box = Box.get_box(box_id)

    if box is None:
        return simplejson.dumps({ 'result': False, 'message': 'This box does not exist.' })

    if len(OrderBox.objects.filter(box=box)) > 0:
        return simplejson.dumps({ 'result': False, 'message': 'Can not delete this box because it is in an order.' })

    box.delete()

    return simplejson.dumps({ 'result': True })
