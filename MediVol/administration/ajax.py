from django.utils import simplejson
from dajaxice.decorators import dajaxice_register

from administration.models import Warehouse
from django.contrib.auth.models import User, Group

@dajaxice_register(method='POST')
def add_warehouse(request, name, abbreviation, address):
    if len(Warehouse.objects.filter(name=name)) != 0:
        return 'name'
    elif len(Warehouse.objects.filter(abbreviation=abbreviation)) != 0:
        return 'abbreviation'
    elif len(Warehouse.objects.filter(address=address)) != 0:
        return 'address'
    
    new_warehouse = Warehouse(name=name, abbreviation=abbreviation.upper(), address=address)
    new_warehouse.save()

    return True

@dajaxice_register(method='POST')
def remove_warehouse(request, abbreviation):
    warehouse = Warehouse.objects.get(abbreviation=abbreviation)
    warehouse.delete()

    return True

@dajaxice_register(method='POST')
def remove_user(request, username):
    userToRemove = User.objects.get(username=username)
    userToRemove.delete()
    
    return True

@dajaxice_register(method='POST')
def change_group(request, username, new_group):
    userToChange = User.objects.get(username=username)
    old_group = userToChange.groups.all()[0]
    new_group = Group.objects.get(name=new_group)
    
    old_group.user_set.remove(userToChange)
    new_group.user_set.add(userToChange)
    
    return True