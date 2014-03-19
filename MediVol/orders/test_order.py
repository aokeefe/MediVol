import os, sys, datetime
sys.path.append('/var/www/MediVol/MediVol/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MediVol.settings")
from django.db import models
from orders.models import Order, OrderBox
from inventory.models import Box

o = Order(order_number=1, creation_date=datetime.datetime.now())
o.save()
boxes = Box.objects.all()
for box in boxes[:6]:
    ob = OrderBox(box=box, order_for=o, cost=1.111)
    ob.save()
