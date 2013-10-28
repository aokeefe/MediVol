import os, sys
sys.path.append('/var/www/MediVol/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MediVol.settings")
from django.db import models
from catalog.models import Category, BoxName

letter_mapping = (
    ('A', 'Mother and Child'),
    ('B', 'Personal Care'),
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

box_name = BoxName.objects.all()
box_name.delete()

box_name_mapping = (
    ('Adult Diapers', 'B'),
    ('OB Pads', 'A'),
    ('OB/GYN Mix', 'A'),
    ('Pediatric Diapers', 'A'),
    ('Pediatric Supplies', 'A'),
    ('Speculums', 'A'),
    ('Anti-Embolism Stockings', 'B'),
    ('Oral Care', 'B'),
    ('Personal Care', 'B'),
    ('Slippers', 'B'),
    ('Under Pads/Chux (Cloth)', 'B'),
    ('Under Pads/Chux (Disposable)', 'B'),
    ('Blood Pressure Cuffs/Stethoscopes', 'C'),
    ('Diabetic Glucometers', 'C'),
    ('Diabetic Supplies', 'C'),
    ('Foam', 'C'),
    ('Patient Care', 'C'),
    ('Probe Covers', 'C'),
    ('Bed Linens', 'C'),
    ('Immobilizers', 'C'),
    ('Patient Gowns', 'C'),
    ('Poseys (Vest, Wrist)', 'C'),
    ('Positioning Devices', 'C'),
    ('Shrouds', 'C'),
    ('Blood Collection/Vacutainer Supplies', 'D'),
    ('Exam Table Paper', 'C'),
    ('Hats/Head Covers', 'E'),
    ('Lab Supplies', 'D'),
    ('Masks', 'E'),
    ('Specimen Containers', 'D'),
    ('Gloves (Sterile)', 'E'),
    ('Gloves (Unsterile, Boxed)', 'E'),
    ('Gloves (Unsterile, Loose)', 'E'),
    ('Gowns (Unsterile, Paper)', 'E'),
    ('Shoe Covers', 'E')

    )

for pair in box_name_mapping:
    box_name = BoxName(name=pair[0], letter=Category.objects.get(letter=pair[1]))
    box_name.save()