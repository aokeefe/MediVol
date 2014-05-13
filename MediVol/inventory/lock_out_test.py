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
           entered_date=datetime.datetime.now(),
           sold=False)
box.save()
#make order
fOrder = Order(creation_date = datetime.datetime.now())
fOrder.save()
#add box to order
fOrderBox = OrderBox(order_for = fOrder, box = box)
fOrderBox.save()
#make second order
sOrder = Order(creation_date = datetime.datetime.now())
sOrder.save()
#add box to second order
sOrderBox = OrderBox(order_for = sOrder, box = box)
sOrderBox.save()

print str(fOrderBox)
print str(sOrderBox)

#Check that the box is in both orders
print box.sold
print OrderBox.objects.filter(box=box)

#lock out box into first order
box.lock_out(sOrder)

#check that box is not in order 2 anymore
print box.sold
print box.orderbox_set.all()

for orderbox in box.orderbox_set.all():
	print 'Boxes in order ' + str(orderbox.order_for) + ': ' + str(orderbox.order_for.get_boxes_in_order())
	print 'Boxes removed from order ' + str(orderbox.order_for) + ': ' + str(orderbox.order_for.get_removed_boxes())