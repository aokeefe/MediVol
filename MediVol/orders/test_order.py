import os, sys, datetime, random
sys.path.append('/var/www/MediVol/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MediVol.settings")
from django.db import models
from orders.models import Order, OrderBox
from inventory.models import Box

o = Order(order_number=1, order_id=random.randint(1,1000), creation_date=datetime.datetime.now())
o.save()
boxes = Box.objects.all()
for box in boxes[:random.randint(2,10)]:
    print box
    ob = OrderBox(box=box, order_for=o)
    ob.save()