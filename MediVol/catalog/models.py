from django.db import models
from import_export.to_csv import to_csv_from_array, to_array_from_csv

#TODO is this a valid number?
NAME_LENGTH = 128
LETTER_LENGTH = 2

class Category(models.Model):
    letter = models.CharField(max_length=LETTER_LENGTH, unique=True)
    name = models.CharField(max_length=NAME_LENGTH)

    @classmethod
    def create_from_csv(cls, csv):
        filtered_values = to_array_from_csv(csv)
        category = Category(letter=str(filtered_values[0]), 
                            name=filtered_values[1])
        category.save()
        return category

    def __unicode__(self):
        return self.name + " - " + self.letter

    def __eq__(self, other):
        return self.letter == other.letter \
           and self.name == other.name

    def to_csv(self):
        values = [self.letter,
                  self.name]
        return to_csv_from_array(values)
    
    def get_search_results_string(self):
        return self.name

class BoxName(models.Model):
    name = models.CharField(max_length=NAME_LENGTH, unique=True)
    category = models.ForeignKey(Category)
    can_expire = models.BooleanField()
    can_count = models.BooleanField()

    @classmethod
    def create_from_csv(cls, csv):
        filtered_values = to_array_from_csv(csv)
        box_name = BoxName(name=filtered_values[0],
                           category=Category.objects.get(letter=filtered_values[1]),
                           can_expire=filtered_values[2],
                           can_count=filtered_values[3])
        box_name.save()
        return box_name

    def __unicode__(self):
        return self.name

    def __eq__(self, other):
        return self.category == other.category \
           and self.name == other.name

    def to_csv(self):
        values = [self.name,
                  self.category.letter,
                  self.can_expire,
                  self.can_count]
        return to_csv_from_array(values)
    
    def get_search_results_string(self):
        return self.category.name + ' > ' + self.name
        
class Item(models.Model):
    name = models.CharField(max_length=NAME_LENGTH)
    box_name = models.ForeignKey(BoxName)
    description = models.CharField(max_length = 500)
    
    @classmethod
    def create_from_csv(cls, csv):
        filtered_values = to_array_from_csv(csv)
        item = Item(name=filtered_values[0], 
                    box_name=BoxName.objects.get(name=filtered_values[1]),
                    description=filtered_values[2])
        item.save()

    def __unicode__(self):
        return self.name

    def __eq__(self, other):
        return self.box_name == other.box_name \
           and self.name == other.name \
           and self.description == other.description

    def to_csv(self):
        values = [self.name,
                  self.box_name.name, 
                  self.description]
        return to_csv_from_array(values)
    
    def get_search_results_string(self):
        return self.box_name.category.name + ' > ' + self.box_name.name + ' > ' + self.name

    class Meta:
        unique_together=('name', 'box_name')
