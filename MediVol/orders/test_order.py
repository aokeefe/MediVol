import os, sys, datetime, random
sys.path.append('/var/www/MediVol/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MediVol.settings")
from django.db import models
from catalog.models import Category, BoxName, Item
from orders.models import Customer, Order, OrderBox
from inventory.models import Box, Contents

mother_child = Category.objects.get(letter='A')
print mother_child

ob_gyn_mix = BoxName.objects.get(name='OB/GYN Mix')
print ob_gyn_mix

item1 = Item.objects.get(name='Cord Blood Collection')
print item1

item2 = Item.objects.get(name='Vaginal Swab')
print item2

try:
    steve = Customer.objects.get(contact_id=1)
    steves_box = Box.objects.get(box_id='A678')
    steves_box_item1 = Contents.objects.get(contents_id=1)
except Exception:
    steve = Customer(contact_id=1,
                     contact_name='Steve Doe',
                     contact_email='Steve@Doe.net',
                     business_name='Steve\'s Shop',
                     business_address='123 Steve Street',
                     shipping_address='123 Steve Street')
    steve.save()

    steves_box = Box(box_id='A678',
                 box_category=Category.objects.get(letter=mother_child.letter),
                 box_size='S',
                 weight=3.23,
                 barcode='12345678',
                 initials='WKB',
                 entered_date=datetime.datetime.now(),
                 old_expiration=None,
                 old_contents=None,
                 shipped_to='',
                 reserved_for='',
                 box_date=datetime.datetime.now())
    steves_box.save()

    steves_box_item1 = Contents(contents_id=1,
                                box_within=steves_box,
                                item=item1,
                                quantity=1,
                                expiration=None)

print steve
print steves_box

try:
    joe = Customer.objects.get(contact_id=2)
except:
    joe = Customer(contact_id=2,
                   contact_name='Joe Doe',
                   contact_email='Joe@Doe.net',
                   business_name='Joe\'s Shop',
                   business_address=None,
                   shipping_address='125 Steve Street')
    joe.save()

print joe

