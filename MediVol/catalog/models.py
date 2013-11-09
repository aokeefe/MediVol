from django.db import models

#TODO is this a valid number?
NAME_LENGTH = 128

class Category(models.Model):
    letter = models.CharField(max_length=1)
    name = models.CharField(max_length=NAME_LENGTH)
    
    @classmethod
    def create_from_csv(cls, csv):
        values = csv.split(",")
        filtered_values = []
        for value in values:
            filtered_values.append(value.replace('<CMA>', ','))
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
        filtered_values = []
        for value in values:
            filtered_values.append(value.replace(',', '<CMA>'))
        return ','.join(filtered_values)

class BoxName(models.Model):
    category = models.ForeignKey(Category)
    name = models.CharField(max_length=NAME_LENGTH)

    @classmethod
    def create_from_csv(cls, csv):
        values = csv.split(",")
        filtered_values = []
        for value in values:
            filtered_values.append(value.replace('<CMA>', ','))
        box_name = BoxName(category=Category.objects.get(letter=filtered_values[0]), 
                           name=filtered_values[1])
        box_name.save()
        return box_name

    def __unicode__(self):
        return self.name

    def __eq__(self, other):
        return self.category == other.category \
           and self.name == other.name

    def to_csv(self):
        values = [self.category.letter,
                  self.name]
        filtered_values = []
        for value in values:
            filtered_values.append(value.replace(',', '<CMA>'))
        return ','.join(filtered_values)
        
#TODO update to a multi Catagory implementation
class Item(models.Model):
    box_name = models.ForeignKey(BoxName)
    name = models.CharField(max_length=NAME_LENGTH)
    description = models.CharField(max_length = 500)
    
    @classmethod
    def create_from_csv(cls, csv):
        values = csv.split(",")
        filtered_values = []
        for value in values:
            filtered_values.append(value.replace('<CMA>', ','))
        item = Item(name=filtered_values[0], 
                    description=filtered_values[2], 
                    box_name=BoxName.objects.get(name=filtered_values[1]))
        item.save()

    def __unicode__(self):
        return self.name

    def __eq__(self, other):
        return self.box_name == other.box_name \
           and self.name == other.name \
           and self.description == other.description

    def to_csv(self):
        return self.name + "&&&" + self.box_name.name + "&&&" + self.description
