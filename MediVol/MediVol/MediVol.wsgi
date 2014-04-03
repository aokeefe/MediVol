import os
import sys

# Add the app's directory to the PYTHONPATH
sys.path.append('/var/www/MediVol/MediVol')
sys.path.append('/var/www/MediVol/MediVol/MediVol')

os.environ['DJANGO_SETTINGS_MODULE'] = 'MediVol.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()


