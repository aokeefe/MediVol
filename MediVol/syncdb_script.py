import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MediVol.settings")
from django.contrib.auth.management.commands import changepassword
from django.core import management
# Run the syncdb
management.call_command('syncdb', interactive=False)

# Create the super user and sets his password.
management.call_command('createsuperuser', interactive=False, username="root", email="nothingatall544@gmail.com")
command = changepassword.Command()
command._get_pass = lambda *args: 'root'
command.execute("root")