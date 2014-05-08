from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
from inventory.models import Warehouse
from administration.models import ResetCode
from catalog.models import Category, BoxName
from django.contrib.auth.models import User, Group
from django.core.validators import validate_email
from notifications.notifier import send_message
from django import forms

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
def set_default_warehouse(request, abbreviation):
    try:
        default_warehouse = Warehouse.objects.get(abbreviation=abbreviation)
    except Warehouse.DoesNotExist:
        return simplejson.dumps({ 'result': 'False' })

    warehouses = Warehouse.objects.all()

    for warehouse in warehouses:
        if warehouse.is_default is True:
            warehouse.is_default = False
            warehouse.save()

    default_warehouse.is_default = True
    default_warehouse.save()

    return simplejson.dumps({ 'result': 'True' })

@dajaxice_register(method='POST')
def remove_user(request, username):
    user_to_remove = User.objects.get(username=username)
    user_to_remove.delete()

    return True

@dajaxice_register(method='POST')
def change_group(request, username, new_group):
    user_to_change = User.objects.get(username=username)
    old_group = user_to_change.groups.all()[0]
    new_group = Group.objects.get(name=new_group)

    old_group.user_set.remove(user_to_change)
    new_group.user_set.add(user_to_change)

    return True

@dajaxice_register(method='POST')
def create_user(request, username, email, group, password, confirm_password):
    if len(User.objects.filter(username=username)) != 0:
        return 'username'
    elif len(User.objects.filter(email=email)) != 0:
        return 'email'
    elif password != confirm_password:
        return 'password mistmatch'

    try:
        validate_email(email)
    except forms.ValidationError:
        return 'invalid email'

    new_user = User(username=username, email=email)
    new_user.set_password(password)
    new_user.save()

    group = Group.objects.get(name=group)
    group.user_set.add(new_user)

    return True

@dajaxice_register(method='POST')
def send_reset(request, username, reset_url):
    reset_code = ResetCode(user=User.objects.get(username=username), code=ResetCode.generate_code())
    reset_code.save()

    return reset_code.send_reset(reset_url)

@dajaxice_register(method='POST')
def reset_password(request, reset_code, password, confirm_password):
    if (password != confirm_password):
        return 'password mismatch'
    elif len(ResetCode.objects.filter(code=reset_code)) != 1:
        return 'invalid code'

    reset_code = ResetCode.objects.get(code=reset_code)

    if reset_code.do_reset(password):
        reset_code.delete()
        return True

    return False

@dajaxice_register(method='POST')
def change_email(request, new_email):
    try:
        validate_email(new_email)
    except forms.ValidationError:
        return 'invalid email'

    request.user.email = new_email
    request.user.save()

    message = 'Your InterVol email has been changed to this email (' + request.user.email + ').'

    send_message('InterVol Email Changed', request.user.email, request.user.username, message)

    return True

@dajaxice_register(method='POST')
def delete_category(request, letter, name):
    try:
        category = Category.objects.get(letter=letter, name=name)
    except Category.DoesNotExist:
        return simplejson.dumps(
            {
                'result': False,
                'message': '"' + letter + ' - ' + name + '" category does not exist.'
            }
        )

    if len(BoxName.objects.filter(category=category)) > 0:
        return simplejson.dumps(
            {
                'result': False,
                'message': '"' + letter + ' - ' + name + '" category could not be deleted because it still has box names in it.'
            }
        )

    category.delete()

    return simplejson.dumps({ 'result': True })
