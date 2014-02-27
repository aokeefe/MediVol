import os, sys
sys.path.append('/var/www/MediVol/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MediVol.settings")
from django.db import models
from orders.models import Order, OrderBox
from inventory.models import Box

o = Order(order_number=1)
o.save()
boxes = Box.objects.all()
for box in boxes[:6]:
    ob = OrderBox(box=box, order_for=o)
    ob.save()