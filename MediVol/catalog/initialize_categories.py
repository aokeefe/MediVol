import os, sys
sys.path.append('/var/www/MediVol/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MediVol.settings")
from django.db import models
from catalog.models import Category

letter_mapping = (
    ('A', 'Mother and Child'),
    ('B', 'Peronal Care'),
    ('C', 'Patient Care'),
    ('D', 'Laboratory'),
    ('E', 'Provider Protection'),
    ('F', 'Pertaining to the Head'),
    ('G', 'Respiratory: Tracheostomy'),
    ('H', 'Respiratory: Oxygen'),
    ('I', 'Cardiovascular'),
    ('J', 'Digestive System'),
    ('K', 'Urinary'),
    ('L', 'Drains and Suction'),
    ('M', 'Dressings'),
    ('O', 'Syringes'),
    ('P', 'Needles'),
    ('Q', 'IV Supplies'),
    ('R', 'Anesthesia'),
    ('S', 'Sutures'),
    ('T', 'Cautery'),
    ('U', 'Surgical Linens'),
    ('V', 'Surgical Miscellanea'),
    ('W', 'Surgical Supplies'),
    ('X', 'Plastic'),
    ('Z', 'Little Things'))
categories = Category.objects.all()
categories.delete()

for pair in letter_mapping:
    category = Category(letter=pair[0], name=pair[1])
    category.save()