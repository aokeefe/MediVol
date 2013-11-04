from django.db import models
from inventory.models import Box

class Order(models.Model):
	#This may need revisiting as a more detailed model becomes available
	reserved_for = models.CharField(max_length=30, null=True)
	paid_for = models.BooleanField(default=False)
	shipped = models.BooleanField(default=False)
	ship_to = models.CharField(max_length=300, null=True)
	order_number = models.IntegerField()
	creation_date = models.DateTimeField('Date the order was made')

	def __unicode__(self):
		return self.order_number
	#def to_csv(self):
		#TODO

class OrderBox(models.Model):
	order_for = models.ForeignKey(Order)
	box = models.ForeignKey(Box)

	def __unicode__(self):
		return self.box + " in order " + self.order_for

	def to_csv(self):
		return self.order_for.order_number + ", " + self.box.box_id