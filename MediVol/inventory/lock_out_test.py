#test file for lock out
import sys, os, datetime
sys.path.append('/var/www/MediVol/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MediVol.settings")
from django.db import models
from catalog.models import Category
from inventory.models import Box
from orders.models import Order, OrderBox

#make box
box = Box( box_size='S',
           box_category=Category.objects.get(letter='A'),
           weight=4.5,
           initials='WKB',
           entered_date=datetime.datetime.now())
box.save()
#make order
fOrder = Order(order_number='testlockout', creation_date = datetime.datetime.now())
fOrder.save()
#add box to order
fOrderBox = OrderBox(order_for = fOrder, box = box)
fOrderBox.save()
#make second order
sOrder = Order(order_number='testlockout2', creation_date = datetime.datetime.now())
sOrder.save()
#add box to second order
sOrderBox = OrderBox(order_for = sOrder, box = box)
sOrderBox.save()

print str(fOrderBox)
print str(sOrderBox)

#Check that the box is in both orders
print box.is_locked_out()
print OrderBox.objects.filter(box=box)

fOrder.order_status = 'S'
fOrder.save()

#check that box is not in order 2 anymore
print box.is_locked_out()
print box.orderbox_set.all()
