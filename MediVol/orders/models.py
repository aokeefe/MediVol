from django.db import models
from inventory.models import Box

class Customer(models.Model):
    contact_name = models.CharField(max_length=40)
    contact_email = models.CharField(max_length=40)
    business_name = models.CharField(max_length=40)
    business_address = models.CharField(max_length=200, null=True)
    shipping_address = models.CharField(max_length=200)

    def __unicode__(self):
        return "contact info for: " + business_name
        
class Order(models.Model):
    #This may need revisiting as a more detailed model becomes available
    reserved_for = models.ForeignKey(Customer, null=True)
    paid_for = models.BooleanField(default=False)
    shipped = models.BooleanField(default=False)
    ship_to = models.CharField(max_length=300, null=True)
    order_number = models.IntegerField()
    creation_date = models.DateTimeField('Date the order was made')

    def __unicode__(self):
        return "Order " + str(self.order_number)
    #def to_csv(self):
        #TODO
    def get_weight(self):
        order_weight = 0.0
        for order_box in self.orderbox_set.all():
            order_weight = order_weight + order_box.box.weight
        return order_weight

class OrderBox(models.Model):
    order_for = models.ForeignKey(Order)
    box = models.ForeignKey(Box)
    cost = models.FloatField(default=0.0)

    def __unicode__(self):
        return self.box + " in order " + self.order_for

    def to_csv(self):
        return self.order_for.order_number + ", " + self.box.box_id