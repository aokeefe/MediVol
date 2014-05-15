from django.utils import simplejson
from dajaxice.decorators import dajaxice_register

from catalog.models import Category, BoxName, Item
from inventory.models import Contents
from search.Searcher import Searcher

@dajaxice_register(method='GET')
def edit_item(request, category_letter, new_box_name, old_box_name, new_item_name, old_item_name, d):
    try:
        old_box_name = BoxName.objects.get(name=old_box_name, category=Category.objects.get(letter=category_letter))
    except BoxName.DoesNotExist:
        return simplejson.dumps({'message':'%s does not exist' % old_box_name})

    try:
        item = Item.objects.get(name=old_item_name, box_name=old_box_name)
    except Item.DoesNotExist:
        return simplejson.dumps({'message':'%s could not be found' % old_item_name})

    try:
        box_name = BoxName.objects.get(name=new_box_name)
    except BoxName.DoesNotExist:
        return simplejson.dumps({'message':'%s does not exist' % new_box_name})

    items_with_this_name = Item.objects.filter(name=new_item_name).filter(box_name=box_name)

    if len(items_with_this_name) > 0:
        for item_with_name in items_with_this_name:
            if item_with_name != item:
                return simplejson.dumps({'message':'%s already exists' % new_item_name})

    item.name = new_item_name
    item.description = d
    item.box_name = box_name
    item.save()

    similar_items = Item.objects.filter(name=old_item_name)
    similar_items_array = []

    for similar_item in similar_items:
        similar_items_array.append({ 'id': similar_item.id, 'box_name': similar_item.box_name.name,
            'name': similar_item.name });

    return simplejson.dumps( { 'message':'%s has been changed' % new_item_name, 'similar': similar_items_array } )

@dajaxice_register(method='POST')
def create_item(request, box_name, item_name, description):
    if box_name == '' or item_name == '':
        return simplejson.dumps({'message': 'Box Name and item name are required.', 'success': 0})

    try:
        box = BoxName.objects.get(name=box_name)
    except BoxName.DoesNotExist:
        return simplejson.dumps({'message':'Box Name "%s" does not exist' % box_name, 'success': 0})

    if Item.objects.filter(name=item_name).filter(box_name = box).count() > 0:
        return simplejson.dumps({'message':'Item "%s" already exists' % item_name, 'success': 0})

    new_item = Item(name=item_name,
                    description=description,
                    box_name=BoxName.objects.get(name=box_name))
    new_item.save()

    return simplejson.dumps({'message':'%s has been added.' % item_name, 'success': 1})

@dajaxice_register(method='POST')
def get_description(request, box_name, item_name):
    try:
        box = BoxName.objects.get(name=box_name)
    except BoxName.DoesNotExist:
        return simplejson.dumps({'message':'','error':'could not fin boxName %s' % box_name})
    item = Item.objects.get(name=item_name, box_name=box)
    return simplejson.dumps({'message': '%s' % item.description, 'item_id': '%s' % item.id})

@dajaxice_register(method='POST')
def create_boxName(request, category_letter, box_name, can_expire, can_count):
    try:
        category = Category.objects.get(letter=category_letter)
    except Category.DoesNotExist:
        return simplejson.dumps({'message':'Category: %s does not exist' % category})
    if BoxName.objects.filter(name=box_name).filter(category=category).count > 0:
        return simplejson.dumps({'message':'BoxName: %s already exists' % box_name})
    new_box_name = BoxName(category = category,
                           name = box_name,
                           can_expire = can_expire,
                           can_count = can_count
                           )
    return simplejson.dumps({'message':'%s has been added' % box_name})

@dajaxice_register(method='POST')
def create_category(request, letter, name):
    if Category.objects.filter(letter=letter).count() > 0:
        return simplejson.dumps({'message':'Category %s already exists' % letter})
    new_category = Category(letter = letter,
                            name = name
                            )
    return simplejson.dumps({'message':'%s has been added' % name})

@dajaxice_register(method='GET')
def delete_item(request, b_name, item_name):
    try:
        item = Item.objects.get(box_name=BoxName.objects.get(name=b_name), name=item_name)
    except Item.DoesNotExist:
        return simplejson.dumps({ 'message': '%s could not be found' % item_name })

    if len(Contents.objects.filter(item=item)) > 0:
        return simplejson.dumps({ 'message': 'This item could not be deleted because it is in a box.' })

    item.delete()

    return simplejson.dumps({ 'message': '%s has been deleted' % item_name })

@dajaxice_register(method='GET')
def delete_box_name(request, letter, name):
    category = Category.objects.get(letter=letter)
    box_name = BoxName.objects.filter(name=name).filter(category=category)
    if box_name.count() < 1:
        return simplejson.dumps({'message':'%s could not be found' % name})
    box_name = box_name[0]
    if Item.objects.filter(box_name=box_name).count > 0:
       return simplejson.dumps({'message':'%s can not be deleted because there are items associated with it' % name})

    box_name.delete()
    return simplejson.dumps({'message':'%s has been deleted' % name})

@dajaxice_register(method='GET')
def delete_category(request, category_letter):
    try:
        category = Category.objects.get(letter=category_letter)
    except Category.DoesNotExist:
        return simplejson.dumps({'message':'Category: %s does not exist' % category_letter})
    category.delete()
    return simplejson.dumps({'message':'%s has been deleted' % category_letter})

@dajaxice_register(method='GET')
def search_box_names(request, query):
    return simplejson.dumps(Searcher.search(query=query, models=[ BoxName ]))
