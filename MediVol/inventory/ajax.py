from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
from datetime import datetime
from random import randint

from catalog.models import Category, BoxName, Item
from inventory.models import Box, Contents
from label.barcodes import BoxLabel

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
def create_box(request, initials, weight, size, items, note=''):
    # TODO: store note in box

    new_box = Box(box_size=size[:1], weight=weight,
        entered_date=datetime.today(), initials=initials.upper())

    new_box.save()

    for item_info in items:
        expiration_date = item_info[1]

        if expiration_date == 'Never':
            expiration_date = None

        contents = Contents(box_within=new_box,
            item=Item.objects.get(name=item_info[0], box_name=BoxName.objects.get(name=item_info[3])),
            quantity=item_info[2],
            expiration=expiration_date)

        contents.save()

    return simplejson.dumps({ 'label': BoxLabel(new_box.barcode).get_image(), 'box_id': new_box.box_id })

@dajaxice_register(method='POST')
def get_label(request, box_id):
    box = Box.objects.get(box_id=box_id)
    return BoxLabel(box.barcode).get_image()
    return BoxLabel(new_box.barcode).get_image()

@dajaxice_register(method='GET')
def get_boxes_with_item(request, item_name, box_name):
    box = BoxName.objects.get(name=box_name)
    item = Item.objects.get(name=item_name, box_name=box)
    box_list = []
    boxes = []
    contents = Contents.objects.filter(item=item)
    for content in contents:
        if content.box_within.box_id not in boxes:
            box = content.box_within
            boxes.append(box.box_id)
            temp = [box.get_id(),
                    box.get_contents_string(),
                    box.get_expiration_display(),
                    box.box_size,
                    box.weight,
                    ''
                    ]
            box_list.append(temp)
    return simplejson.dumps(box_list)
    
        
    