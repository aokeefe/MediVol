from django.db import models
from catalog.models import Item, Category;

class Box(models.Model):
    SMALL = 'S'
    LARGE = 'L'
    UNKNOWN = 'U'
    SIZE_CHOICES = (
        (SMALL, 'Small'),
        (LARGE, 'Large'),
        (UNKNOWN, 'Unknown'),
    )
    box_id = models.CharField(max_length=4, null=True)
    box_category = models.ForeignKey(Category, null=True)
    box_size = models.CharField(max_length=1, choices=SIZE_CHOICES, default=UNKNOWN, null=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True) 
    contents = models.CharField(max_length=300, null=True)
    #zero time is no_exp
    #None is unknown
    #TODO remove
    expiration = models.DateTimeField('expiration date', null=True)
    entered_date = models.DateTimeField('date the box was entered', null=True)
    reserved_for = models.CharField(max_length=300, null=True)
    shipped_to = models.CharField(max_length=300, null=True)
    #TODO: Ask Amy what this could mean
    box_date = models.DateTimeField('Box date', null=True)
    #TODO what does this mean?
    audit = models.IntegerField(default=1, null=True)
    #TODO add the following
    #barcode_value
    #old_box_flag
    #wholesale_value
    initials = models.CharField(max_length=5, null=True)
    #location = models.CharField(max_length=300)
    def to_csv(self):
        return self.box_id + ", " + self.box_size + ", " + str(self.weight) + ", " + self.contents + ", " + str(self.expiration) + ", " + str(self.entered_date) + ", " + self.reserved_for + ", " + self.shipped_to + ", " + str(self.box_date) + ", " + str(self.audit) + "\n"

    def __unicode__(self):
        return self.box_id

    def get_expiration(self):
        expiration = None
        for item in this.boxcontents_set:
            expiration = item.expiration
        return expiration

class BoxContents(models.Model):
    box_within = models.ForeignKey(Box)
    item = models.ForeignKey(Item)
    quantity = models.IntegerField(default=0)
    expiration = models.DateTimeField('expiration date', null=True)

#class Order(models.Model):