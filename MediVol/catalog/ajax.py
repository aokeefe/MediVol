from django.utils import simplejson
from dajaxice.decorators import dajaxice_register

from catalog.models import Category, BoxName, Item


@dajaxice_register
def create_item(request, b_name, item_name):
    
    new_item = Item(name=item_name, 
                    description='', 
                    box_name=BoxName.objects.get(name=b_name))
    new_item.save()
    
    return simplejson.dumps({'message':'%s has been added' % item_name})