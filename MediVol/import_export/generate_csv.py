import sys, os, datetime
sys.path.append('/var/www/MediVol/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MediVol.settings")
from django.db import models
from import_export.model_list import model_list

def generate_csv():
    print("starting export of database")
    time = datetime.datetime.now()
    csv_file = file(time.strftime("/var/www/MediVol/records/%B_%d_%Y")+".csv", 'w')
    for model in model_list:
        print('exporting ' + model.__name__)
        for node in model.objects.all():
            csv_file.write(node.to_csv() +"\n")
        csv_file.write("-----\n")

generate_csv()