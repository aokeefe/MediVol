import pytz
from django.db import models
from catalog.models import Item, Category
from import_export.to_csv import to_csv_from_array, to_array_from_csv
from datetime import datetime, date
import random
from MediVol import id_generator

NAME_LENGTH = 80
ABBREV_LENGTH = 4
ADDRESS_LENGTH = 200

class Warehouse(models.Model):
    name = models.CharField(max_length=NAME_LENGTH)
    abbreviation = models.CharField(max_length=ABBREV_LENGTH, unique=True)
    address = models.CharField(max_length=ADDRESS_LENGTH)
    is_default = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

class Box(models.Model):
    SMALL = 'S'
    LARGE = 'L'
    UNKNOWN = 'U'
    SIZE_CHOICES = (
        (SMALL, 'Small'),
        (LARGE, 'Large'),
        (UNKNOWN, 'Unknown'),
    )
    box_id = models.CharField(max_length=6, null=True, unique=True)
    box_category = models.ForeignKey(Category, null=True)

    box_size = models.CharField(max_length=1, choices=SIZE_CHOICES, default=UNKNOWN, null=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    barcode = models.CharField(max_length=8, unique=True)
    initials = models.CharField(max_length=5, default="")
    entered_date = models.DateTimeField('date the box was entered', null=True)
    old_box_flag = models.BooleanField(default=False)

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
    warehouse = models.ForeignKey(Warehouse, null=True)

    @classmethod
    def get_box(self, box_id_to_get):
        box = None

        try:
            box = Box.objects.get(box_id=box_id_to_get)
        except Box.DoesNotExist:
            boxes = Box.objects.raw(
                '''SELECT * FROM inventory_box
                INNER JOIN catalog_category ON inventory_box.box_category_id = catalog_category.id
                WHERE CONCAT(catalog_category.letter, inventory_box.box_id) = %s''',
                [box_id_to_get]
            )

            for box_found in boxes:
                box = Box.objects.get(box_id=box_found.box_id)
                break

        return box

    @classmethod
    def create_from_csv(cls, csv):
        filtered_values = to_array_from_csv(csv)
        box = Box(box_id=filtered_values[0],
                  box_category=Category.objects.get(letter=filtered_values[1]),
                  box_size=filtered_values[2],
                  weight=filtered_values[3],
                  barcode=filtered_values[4],
                  initials=filtered_values[5],
                  entered_date=filtered_values[6],
                  old_box_flag=filtered_values[7],
                  old_expiration=filtered_values[8],
                  old_contents=filtered_values[9],
                  shipped_to=filtered_values[10],
                  reserved_for=filtered_values[11],
                  box_date=filtered_values[12],
                  audit=filtered_values[13],
                  warehouse=Warehouse.objects.get(abbreviation=filtered_values[14]))
        box.save()
        return box

    def get_size_word(self):
        return self.SIZE_CHOICES[self.box_size]

    def __unicode__(self):
        """
        Returns a printable, human readable, string to represent the Box
        """
        return self.get_id()

    def save(self, *args, **kwargs):
        """
        During that save process we will assign a barcode to the Box, if it does not already have one (ie a new box)
        To make a barcode this method will generate an 8 digit number (with leading zeros), then validate that the
        generated number is not already in use.
        """
        #TODO remove try catch as something is figured out with id uniqueness
        try:
            if self.barcode == None or self.barcode== '':
                while True: #guess until we have a unique barcode
                    self.barcode = "%0.8d" % random.randint(0,99999999) #make a guess
                    if not Box.objects.filter(barcode=self.barcode).exists():
                        break #if the guess was unique stop
        except Exception as e:
            print ('%s (%s)' % ('The Box did not save correctly', type(e)))

        if self.box_id is None:
            self.box_id = id_generator.id_generator(4)
            while True:
                self.box_id = id_generator.id_generator(4)
                if not Box.objects.filter(box_id=self.box_id).exists():
                    break

        super(Box, self).save(*args, **kwargs)

    def to_csv(self):
        """
        Returns a string containing all the CSV information of the Box.  Used in creating database backups
        """
        values = [self.box_id,
                  self.box_category.letter,
                  self.box_size,
                  str(self.weight),
                  str(self.barcode),
                  self.initials,
                  str(self.entered_date),
                  self.old_box_flag,
                  str(self.old_expiration),
                  self.old_contents,
                  self.shipped_to,
                  self.reserved_for,
                  str(self.box_date),
                  str(self.audit),
                  self.warehouse.abbreviation]
        return to_csv_from_array(values)

    def get_id(self):
        if self.old_box_flag:
            return self.box_id
        return self.box_category.letter + self.box_id

    def get_printable_id(self):
        if self.old_box_flag:
            return self.box_id
        return self.box_category.letter + '-' + self.box_id

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

    def get_expiration_display(self):
        expiration = self.get_expiration()

        if expiration is None:
            return 'Never'
        else:
            formatted_expiration = expiration.strftime('%B, %Y')

            if formatted_expiration == 'January, 1970':
                return 'Unknown'
            else:
                return formatted_expiration

    def get_printable_expiration(self):
        expiration = self.get_expiration()

        if expiration is None:
            return 'Never'
        else:
            formatted_expiration = expiration.strftime('%m/%Y')

            if formatted_expiration == 'January, 1970':
                return '??/????'
            else:
                return formatted_expiration

    def get_search_results_string(self):
        return 'Box ' + self.get_id()

    def get_contents_string(self, with_links=False):
        if self.old_contents is None:
            contents_strings = []
            contents = Contents.objects.filter(box_within=self)

            for content in contents:
                if with_links:
                    if content.quantity > 0:
                        contents_strings.append(
                            '<a href="/catalog/item_info/%s" target="_blank">%s</a> x %s' % \
                            (content.item.id, content.item.name, str(content.quantity))
                        )
                    else:
                        contents_strings.append(
                            '<a href="/catalog/item_info/%s" target="_blank">%s</a>' % \
                            (content.item.id, content.item.name)
                        )
                else:
                    if content.quantity > 0:
                        contents_strings.append(content.item.name + ' x ' + str(content.quantity))
                    else:
                        contents_strings.append(content.item.name)

            return ', '.join(contents_strings)

        return self.old_contents

    def get_contents_string_with_links(self):
        return self.get_contents_string(True)

class Contents(models.Model):
    box_within = models.ForeignKey(Box)
    item = models.ForeignKey(Item)
    quantity = models.IntegerField(default=0)
    expiration = models.DateTimeField('expiration date', null=True)

    @classmethod
    def create_from_csv(cls, csv):
        filtered_values = to_array_from_csv(csv)
        contents = Contents(box_within=Box.objects.get(box_id=filtered_values[1]),
                            item=Item.objects.get(name=filtered_values[2]),
                            quantity=filtered_values[3],
                            expiration=filtered_values[4])
        contents.save()
        return contents

    def __unicode__(self):
        """
        Returns a printable, human readable, string to represent the Contents
        """
        return self.item.name

    def get_search_results_string(self):
        return self.item.box_name.category.name + ' > ' + self.item.box_name.name + ' > ' + self.item.name + ' > Box ' + self.box_within.get_id()

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
        return to_csv_from_array(values)
