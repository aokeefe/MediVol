import os, sys
sys.path.append('/var/www/MediVol/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MediVol.settings")
from django.db import models
from catalog.models import Category, BoxName, Item

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
    #this is a placeholder tag for the old inventory
    ('Y', 'UNKNOWN'),
    ('Z', 'LittleThings'))
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
    ('Shoe Covers', 'E'),
    ('Dental Surgery', 'F'),
    ('ENT (Ears, Nose, Throat)', 'F'),
    ('Eye Care', 'F'),
    ('Gowns (Sterile, Paper)', 'E'),
    ('Ophthalmic Surgery', 'F'),
    ('Misc. Tracheostomy Supplies', 'G'),
    ('Respiratory Mix', 'H'),
    ('Tracheostomy Care Kits', 'G'),
    ('Tracheostomy Tubes', 'G'),
    ('Ambu Bags (Adult)', 'H'),
    ('Ambu Bags (Pediatric)', 'H'),
    ('Bronchoscopy Biopsy Forceps/Brushes', 'H'),
    ('O2 Nasal Cannulas & Masks', 'H'),
    ('Oxygen Tubing', 'H'),
    ('Airway', 'H'),
    ('CPAP', 'H'),
    ('Humidifiers', 'H'),
    ('Nebulizers', 'H'),
    ('O2 Gauges & Supplies', 'H'),
    ('Cardiovascular Mix', 'I'),
    ('Defibrillator Pads', 'I'),
    ('EKG Electrodes', 'I'),
    ('Endoscopy', 'J'),
    ('Heart Cannulas', 'I'),
    ('Enema', 'J'),
    ('Feeding & Kangaroo Bags', 'J'),
    ('Feeding Tubes', 'J'),
    ('Misc. Urine Collection', 'K'),
    ('Ostomy Care Supplies', 'J'),
    ('Ostomy Supplies', 'J'),
    ('Catheters (Foley, Straight, Texas)', 'K'),
    ('Dialysis', 'K'),
    ('Nasogastric (NG) Tubes', 'J'),
    ('Urinary Catheter Trays/Kits', 'K'),
    ('Urinary Drainage Bags', 'K'),
    ('Urology Mix', 'K'),
    ('Chest Drains', 'L'),
    ('Jackson-Pratt Drains', 'L'),
    ('Suction Canisters', 'L'),
    ('Suction Catheters', 'L'),
    ('Suction Tubing', 'L'),
    ('Yankauer/Frazier Tips', 'L'),
    ('Bulb Syr inges/Funnels', 'L'),
    ('Drainage Kits', 'L'),
    ('Drains', 'L'),
    ('Irrigation', 'T'),
    ('Roll Gauze', 'M'),
    ('Wound Care', 'M'),
    ('Ace Bandages', 'M'),
    ('Coban', 'M'),
    ('Dressings (Sterile, Non-medicated)', 'M'),
    ('Dressings (Sterile, Treated/Medicated)', 'M'),
    ('Dressings (Unsterile)', 'M'),
    ('Tegaderm', 'M'),
    ('Cast Padding', 'Y'), #Ortho),
    ('Casting Tape', 'Y'), #Ortho),
    ('Ortho Drills & Saw Blades', 'Y'), #Ortho),
    ('Orthopedic Mix', 'Y'), #Ortho),
    ('Shoulder/Elbow Suspension Kits', 'Y'), #Ortho),
    ('Tan Stockinettes', 'Y'), #Ortho),
    ('Insulin Syringes', 'O'),
    ('Syringes - 1-3cc (Sterile)', 'O'),
    ('Syringes - 10cc (Sterile)', 'O'),
    ('Syringes - 20-60cc (Sterile)', 'O'),
    ('Syringes - 5cc (Sterile)', 'O'),
    ('Oral Dosing Syringes', 'O'),
    ('Port Access Needles', 'P'),
    ('Angio-Catheters', 'P'),
    ('Butterfly Catheters', 'P'),
    ('Needles', 'P'),
    ('Spinal Needles', 'P'),
    ('Syringes-All Sizes (Unsterile)', 'O'),
    ('Central Line & Swan Ganz Kits', 'Q'),
    ('Central Line Supplies', 'Q'),
    ('IV Mix', 'Q'),
    ('IV Starter Kits', 'Q'),
    ('IV Tubing', 'Q'),
    ('Anestesia Masks/Circuits', 'R'),
    ('Anesthesia Mix', 'R'),
    ('Endotracheal Tubes/LMAs/ Stylettes', 'R'),
    ('Esmark for Tourniquets', 'R'),
    ('Tourniquet Cuffs', 'R'),
    ('Ventilator Tubing', 'R'),
    ('Needle Box', 'S'),
    ('Skin Staplers (Sterile)', 'T'),
    ('Skin Staplers (Unsterile)', 'T'),
    ('Suture/Staple Removal', 'S'),
    ('Sutures (Expired)', 'S'),
    ('Sutures (Unexpired)', 'S'),
    ('Cautery Supplies', 'T'),
    ('Laceration Kits', 'T'),
    ('Surgical Drapes (Sterile)', 'U'),
    ('Surgical Packs (Sterile)', 'W'),
    ('Misc. OR Supplies (Sterile)', 'W'),
    ('OR Suction Supplies (Sterile)', 'W'),
    ('Skin Markers', 'T'),
    ('Surgical Sheets (Sterile)', 'U'),
    ('Autoclave Wraps', 'U'),
    ('Mayo Stand Covers (Unsterile)', 'U'),
    ('Sheets (Unsterile, Paper)', 'U'),
    ('Sheets (Unsterile, Plastic)', 'U'),
    ('Under Buttocks Drapes', 'U'),
    ('Drapes (Unsterile, Large)', 'U'),
    ('Drapes (Unsterile, Small)', 'U'),
    ('Quarter Drapes', 'U'),
    ('Tail Drapes', 'U'),
    ('Lap Sponges (Sterile)', 'V'),
    ('Lap Sponges (Unsterile)', 'V'),
    ('Raytex (Sterile)', 'V'),
    ('Raytex (Unsterile)', 'V'),
    ('Towels (Unsterile, Cloth)', 'V'),
    ('Towels (Unsterile, Paper)', 'V'),
    ('Foam Sponges', 'W'),
    ('Impervious Stockinettes (Unsterile)', 'W'),
    ('Magnetic Instrument Pads', 'W'),
    ('Scrub Brushes', 'W'),
    ('Skin Prep', 'W'),
    ('Biopsy Kits', 'P'),
    ('Mesh Mix', 'W'),
    ('Neurology Mix', 'W'),
    ('Steri-Drapes/Ioban', 'W'),
    ('Sterilization Pouches', 'W'),
    ('Surgical Patties/Tonsil Sponges', 'W'),
    ('Other Plastics', 'X'),
    ('Pill Bottles', 'X'),
    ('Plastic Trays', 'X'),
    ('Cautery Sticks', 'Z'),
    ('Tourniquets', 'Z'),
    ('Batteries', 'Z'),
    ('Peanuts, Kitners (Sterile)', 'Z'),
    ('Applicator Appliers & Clips (Hemo Clips)', 'Z'),
    ('DermaHooks', 'Z'),
    ('Mastisol/ Dermabond', 'Z'),
    ('Safety Pins, Sterile Rubber Bands, Suture Aid Booties', 'Z'),
    ('Tape & Tape Remover', 'Z'),
    ('Umbilical Tape, Polyester Tape, Silicone Clamp Covers, Retro Tape', 'Z'),
    ('Bone Wax, Gelfoam, Surgifoam, Avitene, Surgicel', 'Z'),
    ('Alcohol Prep Pads & Swabsticks', 'Z'),
    ('Antiseptic Gel Hand Rinse', 'Z'),
    ('Cotton Balls', 'Z'),
    ('Povidone-Iodine & Swabstick', 'Z'),
    ('Povidone-Iodine Pads', 'Z'),
    ('Povidone-Iodine Solution & Ointment', 'Z'),
    ('Povidone-Iodine Sponges & Sponges w/ Sticks', 'Z'),
    ('Thermometers', 'Z'),
    ('Chlorascrub Swabs & Swabsticks', 'Z'),
    ('Antiseptic  & Cleansing Towelettes', 'Z'),
    ('Compound Benzoin Tincture Swabsticks', 'Z'),
    ('Skin Protectant Swabsticks', 'Z'),
    ('Skin Prep Pads & Protective Barrier Wipes', 'Z'),
    ('Petroleum Jelly', 'Z'),
    ('Q-Tips & Cotton-Tipped Applicators', 'Z'),
    ('Tongue Depressors', 'Z'),
    ('Band-Aids, Steri-Strips', 'Z'),
    ('Blades/Scalpels', 'Z'),
    ('Fish/Bowel Protector', 'Z'),
    ('Goggles', 'Z'),
    ('Hot/Cold Packs', 'Z'),
    ('Lubricating Gel & Surgical Lubricant', 'Z'),
    ('Spill Kits', 'Z'),
    ('Ultrasound Gel', 'Z')
    )

for pair in box_name_mapping:
    box_name = BoxName(name=pair[0], category=Category.objects.get(letter=pair[1]))
    box_name.save()

item_pair = (
    ('Pediatric Diapers', 'Small Diapers', 'Small diapers for young babies'),
    ('Oral Care', 'Denture Cleaner Tablets',''),
    ('Oral Care', 'Mouth Moisturizer', ''),
    ('Oral Care', 'Mouth Wash', ''),
    ('Personal Care', 'Body/Shampoo Wipes', ''),
    ('Personal Care', 'Bottles Skin Conditioner', ''),
    ('Personal Care', 'Comfort Care Kits', '')
    )

for pair in item_pair:
    item = Item(box_name=BoxName.objects.get(name=pair[0]), name=pair[1], description=pair[2])
    item.save()