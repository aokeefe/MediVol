from django.db import models
from catalog.models import Item;

class Box(models.Model):
	destination = models.CharField(max_length=300)
	location = models.CharField(max_length=300)
	weight = models.IntegerField(default=0)

class Box_Contents(models.Model):
    box_within = models.ForeignKey(Box)
    item = models.ForeignKey(Item)
    experation = models.DateTimeField('experation date')
    quantity = models.IntegerField(default=0)

#class Order(models.Model):