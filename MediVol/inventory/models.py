from django.db import models

NAME_LENGTH = 128

class Letter(models.Model):
    letter = models.CharField(max_length=5)
    name = models.CharField(max_length=NAME_LENGTH)

class Catagory(models.Model):
	letter = models.ForeignKey(Letter)
	name = models.CharField(max_length=NAME_LENGTH)

class Item(models.Model):
	catagory = models.ForeignKey(Catagory)
	name = models.CharField(max_length=NAME_LENGTH)
	description = models.CharField(max_length = 500)

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