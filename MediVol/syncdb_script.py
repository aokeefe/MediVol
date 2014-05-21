import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MediVol.settings")
from django.contrib.auth.management.commands import changepassword
from django.core import management
from django.contrib.auth.models import User, Group
from inventory.models import Warehouse
# Run the syncdb
management.call_command('syncdb', interactive=False)

# Trying to make the superuser again crashes the script, so check if we already made it
if len(User.objects.filter(username='root')) == 0:
    # Create the super user and sets his password.
    management.call_command('createsuperuser', interactive=False, username="root", email="nothingatall544@gmail.com")
    command = changepassword.Command()
    command._get_pass = lambda *args: 'root'
    command.execute("root")

if len(Warehouse.objects.all()) == 0:
    riedman = Warehouse(name='Riedman', abbreviation='RIED', address='100 Kings Highway S', is_default=True)
    riedman.save()

    clinton = Warehouse(name='Clinton', abbreviation='CLIN', address='1600 Clinton Ave N')
    clinton.save()

# If we made the Admin group, we probably made all the groups and users already
if len(Group.objects.filter(name='Admin')) == 0:
    admin_group = Group(name='Admin')
    admin_group.save()
    admin_group.user_set.add(User.objects.get(username='root'))

    guest_group = Group(name='Guest')
    guest_group.save()

    box_transfer_group = Group(name='Box Transfer')
    box_transfer_group.save()

    read_only_group = Group(name='Read Only')
    read_only_group.save()

    new_user = User(username='admin', email='admin@admin.com')
    new_user.set_password('admin')
    new_user.save()
    admin_group.user_set.add(new_user)

    new_user = User(username='readonly', email='read@only.com')
    new_user.set_password('readonly')
    new_user.save()
    read_only_group.user_set.add(new_user)

    new_user = User(username='boxtransfer', email='box@transfer.com')
    new_user.set_password('boxtransfer')
    new_user.save()
    box_transfer_group.user_set.add(new_user)

    new_user = User(username='guest', email='guest@guest.com')
    new_user.set_password('guest')
    new_user.save()
    guest_group.user_set.add(new_user)
