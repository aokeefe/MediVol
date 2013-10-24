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
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True) 
    contents = models.CharField(max_length=300)
    #zero time is no_exp
    #None is unknown
    expiration = models.DateTimeField('expiration date', null=True)
    entered_date = models.DateTimeField('date the box was entered')
    reserved_for = models.CharField(max_length=300)
    shipped_to = models.CharField(max_length=300)
    #TODO: Ask Amy what this could mean
    box_date = models.DateTimeField('Box date')
    #TODO what does this mean?
    audit = models.IntegerField(default=1)
    #TODO add the following
    #barcode_value
    #old_box_flag
    #wholesale_value
    #initials
    #location = models.CharField(max_length=300)
    def to_csv(self):
        return self.box_id + ", " + self.box_size + ", " + str(self.weight) + ", " + self.contents + ", " + str(self.expiration) + ", " + str(self.entered_date) + ", " + self.reserved_for + ", " + self.shipped_to + ", " + str(self.box_date) + ", " + str(self.audit) + "\n"

    def __unicode__(self):
        return self.box_id
	
#TODO update
class Box_Contents(models.Model):
    box_within = models.ForeignKey(Box)
    item = models.ForeignKey(Item)
    quantity = models.IntegerField(default=0)

#class Order(models.Model):