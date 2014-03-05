import os, sys
sys.path.append('/var/www/MediVol/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MediVol.settings")
from inventory.models import Box, Contents
from catalog.models import Item, Category
from datetime import datetime

category = Category.objects.all()[0]
print category

box = Box(box_category=category, 
          box_id="A123",
          box_size='L',
          weight=12.34,
          old_contents=None,
          initials="WKB",
          entered_date=datetime.now(),
          old_box_flag=True,
          old_expiration=datetime(1999,01,01),
          shipped_to=None,
          reserved_for=None,
          box_date=None,
          audit=1)

box.save()

bn = category.boxname_set.all()[1]
print bn

item1 = bn.item_set.all()[0]
print item1
item2 = bn.item_set.all()[1]
print item2

content1 = Contents(box_within=box,
                    item=item1,
                    quantity=6,
                    expiration=None)
content1.save()

content2 = Contents(box_within=box,
                    item=item2,
                    quantity=6,
                    expiration=None)
content2.save()