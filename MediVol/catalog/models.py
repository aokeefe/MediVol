from django.db import models

NAME_LENGTH = 128

class Category(models.Model):
    letter = models.CharField(max_length=1)
    name = models.CharField(max_length=NAME_LENGTH)
    def __unicode__(self):
        return self.name + " - " + self.letter

    def to_csv(self):
    	return self.letter + ", " + self.name

class BoxName(models.Model):
    letter = models.ForeignKey(Category)
    name = models.CharField(max_length=NAME_LENGTH)

#TODO remove in favor of a multi Catagory implementation
class Item(models.Model):
    category = models.ForeignKey(Category)
    name = models.CharField(max_length=NAME_LENGTH)
    description = models.CharField(max_length = 500)
