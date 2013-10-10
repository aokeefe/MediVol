from django.db import models

NAME_LENGTH = 128

class Letter(models.Model):
    letter = models.CharField(max_length=5)
    name = models.CharField(max_length=NAME_LENGTH)

class Category(models.Model):
    letter = models.ForeignKey(Letter)
    name = models.CharField(max_length=NAME_LENGTH)

class Item(models.Model):
    catagory = models.ForeignKey(Catagory)
    name = models.CharField(max_length=NAME_LENGTH)
    description = models.CharField(max_length = 500)