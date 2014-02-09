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
    ('N', 'Ortho'),
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
    ('Adult Diapers','B','N','N'),
    ('OB Pads','A','Y','N'),
    ('OB/GYN Mix','A','Y','N'),
    ('Pediatric Diapers','A','Y','N'),
    ('Pediatric Supplies','A','Y','N'),
    ('Speculums','A','N','Y'),
    ('Anti-Embolism Stockings','B','Y','Y'),
    ('Oral Care','B','Y','N'),
    ('Personal Care','B','Y','N'),
    ('Slippers','B','N','N'),
    ('Under Pads/Chux (Cloth)','B','N','Y'),
    ('Under Pads/Chux (Disposable)','B','N','N'),
    ('Blood Pressure Cuffs/Stethoscopes','C','N','Y'),
    ('Diabetic Glucometers','C','Y','Y'),
    ('Diabetic Supplies','C','Y','Y'),
    ('Foam','C','Y','Y'),
    ('Patient Care','C','Y','N'),
    ('Probe Covers','C','Y','Y'),
    ('Bed Linens','C','N','N'),
    ('Immobilizers','C','N','Y'),
    ('Patient Gowns','C','N','Y'),
    ('Poseys (Vest, Wrist)','C','N','Y'),
    ('Positioning Devices','C','N','Y'),
    ('Shrouds','C','N','Y'),
    ('Blood Collection/Vacutainer Supplies','D','Y','N'),
    ('Exam Table Paper','C','N','N'),
    ('Hats/Head Covers','E','Y','N'),
    ('Lab Supplies','D','Y','N'),
    ('Masks','E','Y','N'),
    ('Specimen Containers','D','Y','N'),
    ('Gloves (Sterile)','E','Y','Y'),
    ('Gloves (Unsterile, Boxed)','E','Y','Y'),
    ('Gloves (Unsterile, Loose)','E','Y','Y'),
    ('Gowns (Unsterile, Paper)','E','Y','Y'),
    ('Shoe Covers','E','Y','N'),
    ('Dental Surgery','F','Y','N'),
    ('ENT (Ears, Nose, Throat)','F','Y','N'),
    ('Eye Care','F','Y','N'),
    ('Gowns (Sterile, Paper)','E','Y','Y'),
    ('Ophthalmic Surgery','F','Y','N'),
    ('Misc. Tracheostomy Supplies','G','Y','N'),
    ('Respiratory Mix','H','Y','N'),
    ('Tracheostomy Care Kits','G','Y','Y'),
    ('Tracheostomy Tubes','G','Y','Y'),
    ('Ambu Bags (Adult)','H','N','Y'),
    ('Ambu Bags (Pediatric)','H','N','Y'),
    ('Bronchoscopy Biopsy Forceps/Brushes','H','Y','N'),
    ('O2 Nasal Cannulas & Masks','H','N','Y'),
    ('Oxygen Tubing','H','N','Y'),
    ('Airway','H','Y','N'),
    ('CPAP','H','Y','N'),
    ('Humidifiers','H','Y','Y'),
    ('Nebulizers','H','Y','Y'),
    ('O2 Gauges & Supplies','Z','N','Y'),
    ('Cardiovascular Mix','I','Y','N'),
    ('Defibrillator Pads','I','Y','N'),
    ('EKG Electrodes','I','Y','N'),
    ('Endoscopy','J','Y','N'),
    ('Heart Cannulas','I','Y','N'),
    ('Enema','J','Y','N'),
    ('Feeding & Kangaroo Bags','J','Y','Y'),
    ('Feeding Tubes','J','Y','N'),
    ('Misc. Urine Collection','K','Y','N'),
    ('Ostomy Care Supplies','J','Y','N'),
    ('Ostomy Supplies','J','Y','N'),
    ('Catheters (Foley, Straight, Texas)','K','Y','N'),
    ('Dialysis','K','Y','N'),
    ('Nasogastric (NG) Tubes','J','Y','N'),
    ('Urinary Catheter Trays/Kits','K','Y','Y'),
    ('Urinary Drainage Bags','K','Y','Y'),
    ('Urology Mix','K','Y','N'),
    ('Chest Drains','L','Y','Y'),
    ('Jackson-Pratt Drains','L','Y','Y'),
    ('Suction Canisters','L','Y','Y'),
    ('Suction Catheters','L','Y','N'),
    ('Suction Tubing','L','Y','Y'),
    ('Yankauer/Frazier Tips','L','Y','Y'),
    ('Bulb Syringes/Funnels','L','Y','Y'),
    ('Drainage Kits','L','Y','Y'),
    ('Drains','L','Y','Y'),
    ('Irrigation','T','Y','Y'),
    ('Roll Gauze','M','Y','N'),
    ('Wound Care','M','Y','N'),
    ('Ace Bandages','M','N','N'),
    ('Coban','M','Y','N'),
    ('Dressings (Sterile, Non-medicated)','M','Y','N'),
    ('Dressings (Sterile, Treated/Medicated)','M','Y','N'),
    ('Dressings (Unsterile)','M','Y','N'),
    ('Tegaderm','M','Y','N'),
    ('Cast Padding','N','Y','Y'),
    ('Casting Tape','N','Y','Y'),
    ('Ortho Drills & Saw Blades','N','Y','N'),
    ('Orthopedic Mix','N','Y','N'),
    ('Shoulder/Elbow Suspension Kits','N','Y','N'),
    ('Tan Stockinettes','N','N','Y'),
    ('Insulin Syringes','O','Y','N'),
    ('Syringes - 1-3cc (Sterile)','O','Y','N'),
    ('Syringes - 10cc (Sterile)','O','Y','N'),
    ('Syringes - 20-60cc (Sterile)','O','Y','N'),
    ('Syringes - 5cc (Sterile)','O','Y','N'),
    ('Oral Dosing Syringes','O','Y','N'),
    ('Port Access Needles','P','Y','Y'),
    ('Angio-Catheters','P','Y','Y'),
    ('Butterfly Catheters','P','Y','Y'),
    ('Needles','P','Y','N'),
    ('Spinal Needles','P','Y','Y'),
    ('Syringes-All Sizes (Unsterile)','O','Y','N'),
    ('Central Line & Swan Ganz Kits','Q','Y','N'),
    ('Central Line Supplies','Q','Y','N'),
    ('IV Mix','Q','Y','N'),
    ('IV Starter Kits','Q','Y','Y'),
    ('IV Tubing','Q','Y','N'),
    ('Anesthesia Masks/Circuits','R','Y','Y'),
    ('Anesthesia Mix','R','Y','N'),
    ('Endotracheal Tubes/LMAs/ Stylettes','R','Y','Y'),
    ('Esmark for Tourniquets','R','Y','Y'),
    ('Tourniquet Cuffs','R','Y','Y'),
    ('Ventilator Tubing','R','Y','Y'),
    ('Needle Box','S','Y','Y'),
    ('Skin Staplers (Sterile)','T','Y','Y'),
    ('Skin Staplers (Unsterile)','T','Y','Y'),
    ('Suture/Staple Removal','S','Y','Y'),
    ('Sutures (Expired)','S','N','N'),
    ('Sutures (Unexpired)','S','Y','N'),
    ('Cautery Supplies','T','Y','Y'),
    ('Laceration Kits','T','Y','Y'),
    ('Surgical Drapes (Sterile)','U','Y','Y'),
    ('Surgical Packs (Sterile)','U','Y','Y'),
    ('Misc. OR Supplies (Sterile)','W','Y','Y'),
    ('OR Suction Supplies (Sterile)','W','Y','Y'),
    ('Skin Markers','T','Y','N'),
    ('Surgical Sheets (Sterile)','U','Y','Y'),
    ('Autoclave Wraps','U','N','Y'),
    ('Mayo Stand Covers (Unsterile)','U','Y','Y'),
    ('Sheets (Unsterile, Paper)','U','Y','Y'),
    ('Sheets (Unsterile, Plastic)','U','Y','Y'),
    ('Under Buttocks Drapes','U','Y','Y'),
    ('Drapes (Unsterile, Large)','U','Y','Y'),
    ('Drapes (Unsterile, Small)','U','Y','Y'),
    ('Quarter Drapes','U','Y','Y'),
    ('Tail Drapes','U','Y','Y'),
    ('Lap Sponges (Sterile)','V','Y','Y'),
    ('Lap Sponges (Unsterile)','V','Y','N'),
    ('Raytex (Sterile)','V','Y','Y'),
    ('Raytex (Unsterile)','V','Y','N'),
    ('Towels (Unsterile, Cloth)','V','Y','Y'),
    ('Towels (Unsterile, Paper)','V','Y','N'),
    ('Foam Sponges','W','Y','N'),
    ('Impervious Stockinettes (Unsterile)','W','Y','Y'),
    ('Magnetic Instrument Pads','W','N','Y'),
    ('Scrub Brushes','W','Y','Y'),
    ('Skin Prep','W','Y','Y'),
    ('Biopsy Kits','P','Y','Y'),
    ('Mesh Mix','W','Y','N'),
    ('Neurology Mix','W','Y','N'),
    ('Steri-Drapes/Ioban','W','Y','Y'),
    ('Sterilization Pouches','W','N','Y'),
    ('Surgical Patties/Tonsil Sponges','W','Y','N'),
    ('Other Plastics','X','Y','Y'),
    ('Pill Bottles','X','N','N'),
    ('Plastic Trays','X','N','Y'),
    ('Cautery Sticks','Z','Y','Y'),
    ('Tourniquets','Z','Y','N'),
    ('Batteries','NONE','N','N'),
    ('Peanuts, Kitners (Sterile)','Z','Y','Y'),
    ('Applicator Appliers & Clips (Hemo Clips)','Z','Y','Y'),
    ('DermaHooks','Z','Y','N'),
    ('Mastisol/ Dermabond','Z','Y','N'),
    ('Safety Pins, Sterile Rubber Bands, Suture Aid Booties','Z','Y','N'),
    ('Tape & Tape Remover','Z','Y','N'),
    ('Umbilical Tape, Polyester Tape, Silicone Clamp Covers, Retro Tape','Z','Y','N'),
    ('Bone Wax, Gelfoam, Surgifoam, Avitene, Surgicel','Z','Y','N'),
    ('Alcohol Prep Pads & Swabsticks','Z','Y','N'),
    ('Antiseptic Gel Hand Rinse','Z','Y','N'),
    ('Cotton Balls','Z','Y','N'),
    ('Povidone-Iodine & Swabstick','Z','Y','N'),
    ('Povidone-Iodine Pads','Z','Y','N'),
    ('Povidone-Iodine Solution & Ointment','Z','Y','N'),
    ('Povidone-Iodine Sponges & Sponges w/ Sticks','Z','Y','N'),
    ('Thermometers','Z','Y','Y'),
    ('Chlorascrub Swabs & Swabsticks','Z','Y','N'),
    ('Antiseptic  & Cleansing Towelettes','Z','Y','N'),
    ('Compound Benzoin Tincture Swabsticks','Z','Y','N'),
    ('Skin Protectant Swabsticks','Z','Y','N'),
    ('Skin Prep Pads & Protective Barrier Wipes','Z','Y','N'),
    ('Petroleum Jelly','Z','Y','N'),
    ('Q-Tips & Cotton-Tipped Applicators','Z','Y','N'),
    ('Tongue Depressors','Z','Y','N'),
    ('Band-Aids, Steri-Strips','Z','Y','N'),
    ('Blades/Scalpels','Z','Y','N'),
    ('Fish/Bowel Protector','Z','Y','N'),
    ('Goggles','Z','Y','Y'),
    ('Hot/Cold Packs','Z','Y','Y'),
    ('Lubricating Gel & Surgical Lubricant','Z','Y','N'),
    ('Spill Kits','Z','Y','Y'),
    ('Ultrasound Gel','Z','Y','N')
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