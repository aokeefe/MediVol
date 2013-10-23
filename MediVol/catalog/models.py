from django.db import models

NAME_LENGTH = 128

class Category(models.Model):
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
    letter = models.CharField(max_length=1, choices=letter_mapping)
    name = models.CharField(max_length=NAME_LENGTH)

class Box_name(models.Model):
    letter = models.ForeignKey(Category)
    name = models.CharField(max_length=NAME_LENGTH)

#TODO remove in favor of a multi Catagory implementation
class Item(models.Model):
    category = models.ForeignKey(Category)
    name = models.CharField(max_length=NAME_LENGTH)
    description = models.CharField(max_length = 500)
