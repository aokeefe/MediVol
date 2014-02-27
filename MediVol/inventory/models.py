import pytz
from django.db import models
from catalog.models import Item, Category
from datetime import datetime
import random

class Box(models.Model):
    SMALL = 'S'
    LARGE = 'L'
    UNKNOWN = 'U'
    SIZE_CHOICES = (
        (SMALL, 'Small'),
        (LARGE, 'Large'),
        (UNKNOWN, 'Unknown'),
    )
    box_category = models.ForeignKey(Category, null=True)
    box_id = models.CharField(max_length=6, null=True, unique=True)

    box_size = models.CharField(max_length=1, choices=SIZE_CHOICES, default=UNKNOWN, null=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True) 
    old_contents = models.CharField(max_length=300, null=True)
    barcode = models.CharField(max_length=8)
    initials = models.CharField(max_length=5, default="")
    entered_date = models.DateTimeField('date the box was entered', null=True)
    old_box_flag = models.BooleanField(default=False)

    #location = models.CharField(max_length=300)
    #None is no expiration
    #TODO remove
    old_expiration = models.DateTimeField('expiration date', null=True)
    old_contents = models.CharField(max_length=300, null=True)
    shipped_to = models.CharField(max_length=300, null=True)
    reserved_for = models.CharField(max_length=300, null=True)

    #TODO: Ask Amy what this could mean
    box_date = models.DateTimeField('Box date', null=True)
    #TODO what does this mean?
    audit = models.IntegerField(default=1, null=True)

    @classmethod
    def create_from_csv(cls, csv):
        values = csv.split(",")
        filtered_values = []
        for value in values:
            filtered_values.append(value.replace('<CMA>', ','))

        if filtered_values[3] == "None":
            box_weight = None
        else:
            box_weight = float(filtered_values[3])
            
        box = Box(box_category=Category.objects.get(letter=filtered_values[0]),
                  box_id=filtered_values[1],
                  box_size=filtered_values[2],
                  weight=box_weight,
                  initials=filtered_values[4],
                  entered_date=filtered_values[5],
                  old_expiration=filtered_values[6],
                  old_contents=filtered_values[7],
                  box_date=filtered_values[8],
                  audit=filtered_values[9],
                  shipped_to=filtered_values[10],
                  reserved_for=filtered_values[11])
        box.save()
        return box

    def __unicode__(self):
        """
        Returns a printable, human readable, string to represent the Box
        """
        return self.box_id

    def save(self, *args, **kwargs):
        """
        During that save process we will assign a barcode to the Box, if it does not already have one (ie a new box)
        To make a barcode this method will generate an 8 digit number (with leading zeros), then validate that the 
        generated number is not already in use.
        """
        try:
            if self.barcode == None or self.barcode== '':
                while True: #guess until we have a unique barcode
                    self.barcode = "%0.8d" % random.randint(0,99999999) #make a guess
                    if not Box.objects.filter(barcode=self.barcode).exists():
                        break #if the guess was unique stop
            super(Box, self).save(*args, **kwargs)
        except Exception as e: 
            print '%s (%s)' % (e.message, type(e))

    def to_csv(self):
        """
        Returns a string containing all the CSV information of the Box.  Used in creating database backups
        """
        values = [self.box_category.letter,
                  self.box_id, 
                  self.box_size, 
                  str(self.weight),
                  self.initials,
                  str(self.entered_date),
                  str(self.old_expiration),
                  self.old_contents,
                  str(self.box_date),
                  str(self.audit),
                  self.shipped_to,
                  self.reserved_for]
        filtered_values = []
        for value in values:
            filtered_values.append(value.replace(',', '<CMA>').replace('\n', ''))
        return ','.join(filtered_values)

    def get_id(self):
        if len(self.box_id) == 4:
            return self.box_id
        return self.box_category.letter + self.box_id

    def get_expiration(self):
        """
        Finds the oldest date amoung the contents of a Box, and return it.
        For example if an item is expireing on 01-01-2014 and another is expireing on 01-01-2012, 01-01-2012 will be 
        returned
        """
        if self.old_expiration is not None:
            return self.old_expiration
        NOT_EXPIRING_IN_THIS_MILLENIUM = datetime(3013,1,1,0,0,0,0,pytz.UTC)
        expiration = NOT_EXPIRING_IN_THIS_MILLENIUM
        for item in self.contents_set.all():
            #if the item has an expiration that is older than the oldest replace it
            if item.expiration is not None and item.expiration < expiration:
                expiration = item.expiration
        if expiration is NOT_EXPIRING_IN_THIS_MILLENIUM:
            return None
        return expiration

class Contents(models.Model):
    box_within = models.ForeignKey(Box)
    item = models.ForeignKey(Item)
    quantity = models.IntegerField(default=0)
    expiration = models.DateTimeField('expiration date', null=True)

    @classmethod
    def create_from_csv(cls, csv):
        values = csv.split(",")
        filtered_values = []
        for value in values:
            filtered_values.append(value.replace('<CMA>', ','))
        contents = Contents(box_within=Box.objects.get(box_id=filtered_values[0]),
                            item=Item.objects.get(name=filtered_values[1]),
                            quantity=filtered_values[2],
                            expiration=filtered_values[3])
        contents.save()
        return contents

    def __unicode__(self):
        """
        Returns a printable, human readable, string to represent the Contents
        """
        return self.item.name

    def save(self, *args, **kwargs):
        super(Contents, self).save(*args, **kwargs)
        box = self.box_within
        item = self.item
        box.box_category = item.box_name.category
        box.save()

    #TODO test
    def to_csv(self):
        """
        Returns a string containing all the CSV information of the Contents.  Used in creating database backups
        """
        values = [self.box_within.box_id,
                  self.item.name,
                  self.quantity,
                  self.expiration]
        filtered_values = []
        for value in values:
            filtered_values.append(value.replace(',', '<CMA>'))
        return ','.join(filtered_values)
