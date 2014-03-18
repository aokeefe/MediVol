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
    # TODO: generate a real box ID
    # TODO: store note in box
    box_id = randint(100, 999)

    # Generates IDs until we find one that isn't in use yet
    while Box.objects.filter(box_id=box_id).exists():
        box_id = randint(100, 999)

    new_box = Box(box_id=box_id, box_size=size[:1], weight=weight,
        entered_date=datetime.today(), initials=initials.upper())

    new_box.save()

    for item in items:
        expiration_date = item[1]

        if expiration_date == 'Never':
            expiration_date = None

        contents = Contents(box_within=new_box,
            item=Item.objects.get(name=item[0]),
            quantity=item[2],
            expiration=expiration_date)

        contents.save()

    return BoxLabel(new_box.barcode).get_image()

@dajaxice_register(method='POST')
def get_label(request, box_id):
    box = Box.objects.get(box_id=box_id)
    return BoxLabel(box.barcode).get_image()
