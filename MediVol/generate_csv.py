import sys, os, datetime
sys.path.append('/var/www/MediVol/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MediVol.settings")
from django.db import models
from catalog.models import Category, BoxName
from inventory.models import Box

def generate_csv():
    print("start")
    time = datetime.datetime.now()
    csv_file = open(time.strftime("%B_%d_%Y")+".csv", 'w')
    models = [Category, BoxName, Box]
    for model in models:
        for node in model.objects.all():
            csv_file.write(node.to_csv() +"\n")
        csv_file.write("-----\n")

generate_csv()