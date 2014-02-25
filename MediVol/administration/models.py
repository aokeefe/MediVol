from django.db import models

NAME_LENGTH = 40
ABBREV_LENGTH = 4
ADDRESS_LENGTH = 200

class Warehouse(models.Model):
    name = models.CharField(max_length=NAME_LENGTH)
    abbreviation = models.CharField(max_length=ABBREV_LENGTH)
    address = models.CharField(max_length=ADDRESS_LENGTH)
    
    def __unicode__(self):
        return self.name