from django.db import models
from catalog.models import Item;

class Box(models.Model):
    SMALL = 'S'
    LARGE = 'L'
    UNKNOWN = 'U'
    SIZE_CHOICES = (
        (SMALL, 'Small'),
        (LARGE, 'Large'),
        (UNKNOWN, 'Unknown'),
    )
    box_id = models.CharField(max_length=4)
    box_size = models.CharField(max_length=1, choices=SIZE_CHOICES, default=UNKNOWN)
    weight = models.DecimalField(max_digits=5, decimal_places=2) 
    contents = models.CharField(max_length=300)
    experation = models.DateTimeField('experation date')
    entered_date = models.DateTimeField('experation date')
    reserved_for = models.CharField(max_length=300)
    shipped_to = models.CharField(max_length=300)
    box_date = models.DateTimeField('experation date')
    audit = models.IntegerField(default=1)
    #location = models.CharField(max_length=300)
	

class Box_Contents(models.Model):
    box_within = models.ForeignKey(Box)
    item = models.ForeignKey(Item)
    quantity = models.IntegerField(default=0)

#class Order(models.Model):