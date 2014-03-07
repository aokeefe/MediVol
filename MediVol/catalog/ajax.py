from django.utils import simplejson
from dajaxice.decorators import dajaxice_register

from catalog.models import Category, BoxName, Item
from search.Searcher import Searcher

@dajaxice_register(method='POST')
def create_item(request, box_name, item_name, description):
    try:
        box = BoxName.objects.get(name=box_name)
    except BoxName.DoesNotExist:
        return simplejson.dumps({'message':'Box name: %s does not exist' % box_name, 'success': 0})
    if Item.objects.filter(name=item_name).filter(box_name = box).count() > 0:
        return simplejson.dumps({'message':'Item: %s already exists' % item_name, 'success': 0})
    new_item = Item(name=item_name,
                    description=description,
                    box_name=BoxName.objects.get(name=box_name))
    new_item.save()

    return simplejson.dumps({'message':'%s has been added' % item_name, 'success': 1})

@dajaxice_register(method='POST')
def get_description(request, box_name, item_name):
    try:
        box = BoxName.objects.get(name=box_name)
    except BoxName.DoesNotExist:
        return simplejson.dumps({'message':'','error':'could not fin boxName %s' % box_name})
    item = Item.objects.get(name=item_name, box_name=box)
    return simplejson.dumps({'message': '%s' % item.description})



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
def edit_item(request, category_letter, new_box_name, old_box_name, new_item_name, old_item_name, d):
    old_box_name = BoxName.objects.filter(name=old_box_name).filter(category=Category.objects.get(letter=category_letter))
    item = Item.objects.filter(name=old_item_name).filter(box_name=old_box_name)
    if item.count() < 1:
        return simplejson.dumps({'message':'%s could not be found' % old_item_name})
    box_name = BoxName.objects.filter(name=new_box_name).filter(category=Category.objects.get(letter=category_letter))
    if box_name.count() < 1:
        return simplejson.dumps({'message':'%s does not exist' % new_box_name})
    if Item.objects.filter(name=new_item_name).filter(box_name=box_name).count() > 0:
        return simplejson.dumps({'message':'%s already exists' % new_item_name})
    item = item[0]
    item.name = new_item_name
    item.description = d
    item.box_name = box_name[0]
    item.save()
    return simplejson.dumps({'message':'%s has been changed' % new_item_name})

@dajaxice_register(method='GET')
def delete_item(request, b_name, item_name):

    items = Item.objects.filter(name=item_name)
    for item in items:
        if item.box_name.name == b_name:
            item.delete()
            return simplejson.dumps({'message':'%s has been deleted' % item_name})
    return simplejson.dumps({'message':'%s could not be found' % item_name})

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
