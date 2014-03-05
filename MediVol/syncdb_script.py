import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MediVol.settings")
from django.contrib.auth.management.commands import changepassword
from django.core import management
from django.contrib.auth.models import User, Group
# Run the syncdb
management.call_command('syncdb', interactive=False)

# Trying to make the superuser again crashes the script, so check if we already made it
if len(User.objects.filter(username='root')) == 0:
    # Create the super user and sets his password.
    management.call_command('createsuperuser', interactive=False, username="root", email="nothingatall544@gmail.com")
    command = changepassword.Command()
    command._get_pass = lambda *args: 'root'
    command.execute("root")

# If we made the Admin group, we probably made all the groups and users already
if len(Group.objects.filter(name='Admin')) == 0:
    admin_group = Group(name='Admin')
    admin_group.save()
    admin_group.user_set.add(User.objects.get(username='root'))

    guest_group = Group(name='Guest')
    guest_group.save()

    box_transfer_group = Group(name='Box Transfer')
    box_transfer_group.save()

    new_user = User(username='mikelentini', email='mike@mikelentini.com')
    new_user.set_password('mikelentini')
    new_user.save()

    guest_group.user_set.add(new_user)

    new_user = User(username='bill', email='bill@bill.com')
    new_user.set_password('bill')
    new_user.save()

    box_transfer_group.user_set.add(new_user)

    new_user = User(username='shun', email='shun@shun.com')
    new_user.set_password('shun')
    new_user.save()

    guest_group.user_set.add(new_user)

    new_user = User(username='boom', email='boom@boom.com')
    new_user.set_password('boom')
    new_user.save()

    box_transfer_group.user_set.add(new_user)

    new_user = User(username='anthony', email='anthony@anthony.com')
    new_user.set_password('anthony')
    new_user.save()

    guest_group.user_set.add(new_user)
