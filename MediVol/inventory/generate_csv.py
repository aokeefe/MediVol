import sys, os, datetime
sys.path.append('/var/www/MediVol/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MediVol.settings")
from django.db import models
from inventory.models import Box

def generate_csv():
  time = datetime.datetime.now()
  csv_file = open(time.strftime("%B_%d_%Y")+".csv", 'w')
  for box in Box.objects.all():
    csv_file.write(box.to_csv())

generate_csv()