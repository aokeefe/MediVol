import sys, os, datetime
sys.path.append('/var/www/MediVol/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MediVol.settings")
from django.db import models
from catalog.models import Category, BoxName, Item
from inventory.models import Box, Contents

def generate_csv():
    print("starting export of database")
    time = datetime.datetime.now()
    csv_file = open(time.strftime("%B_%d_%Y")+".csv", 'w')
    #TODO: might want to make this an import to keep it the same across importer and exporter
    models = [Category, BoxName, Item, Box, Contents]
    for model in models:
        print('exporting ' + model.__name__)
        for node in model.objects.all():
            csv_file.write(node.to_csv() +"\n")
        csv_file.write("-----\n")

generate_csv()