import sys, os, datetime
sys.path.append('/var/www/MediVol/MediVol/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MediVol.settings")
from django.db import models
from catalog.models import Category, BoxName, Item
from inventory.models import Box, Contents

def import_csv():
    #replace with parameter
    time = datetime.datetime.now()
    csv_file = open(time.strftime("records/%B_%d_%Y")+".csv", 'r')
    #TODO move outside import\export
    models = [Category, BoxName, Item, Box, Contents]
    csv = csv_file.read()
    models_csv = csv.split("-----\n")
    for x in range(0, len(models) -1):
        current_set = models[x].objects.all()
        current_set.delete()
        splitlines = models_csv[x].splitlines()
        for y in splitlines:
            models[x].create_from_csv(y)

import_csv()
