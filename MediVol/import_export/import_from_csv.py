import sys, os, datetime
sys.path.append('/var/www/MediVol/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MediVol.settings")
from django.db import models
from import_export.model_list import model_list

def import_csv(csv_loc):
    print csv_loc
    time = datetime.datetime.now()
    csv_file = open(csv_loc, 'r')
    csv = csv_file.read()
    models_csv = csv.split("-----\n")
    print 'Number of models: ' + str(len(model_list))
    for x in range(0, len(model_list)):
        print 'Number of nodes in ' + model_list[x].__name__ + ' before: ' + str(len(model_list[x].objects.all()))
        current_set = model_list[x].objects.all()
        current_set.delete()
        splitlines = models_csv[x].splitlines()
        for y in splitlines:
            model_list[x].create_from_csv(y)
        print 'Number of nodes in ' + model_list[x].__name__ + ' post: ' + str(len(model_list[x].objects.all()))

import_csv(sys.argv[1])