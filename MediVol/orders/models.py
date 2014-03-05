from django.db import models
from inventory.models import Box
from import_export import to_csv

class Customer(models.Model):
    contact_name = models.CharField(max_length=80)
    contact_email = models.CharField(max_length=80)
    business_name = models.CharField(max_length=80)
    business_address = models.CharField(max_length=200, null=True)
    shipping_address = models.CharField(max_length=200)

    def __unicode__(self):
        return "contact info for: " + business_name
        
class Order(models.Model):
    CREATED = 'C'
    UNPAID = 'U'
    PAID = 'P'
    SHIPPED = 'S'
    ORDER_STATUS = (
        (CREATED, 'Created'),
        (UNPAID, 'Unpaid For'),
        (PAID, 'Paid For'),
        (SHIPPED, 'Shipped Out'),
    )
    #This may need revisiting as a more detailed model becomes available
    order_id = models.IntegerField(unique=True)
    reserved_for = models.CharField(max_length=30, null=True)
    paid_for = models.BooleanField(default=False)
    shipped = models.BooleanField(default=False)
    ship_to = models.CharField(max_length=300, null=True)
    order_number = models.IntegerField()
    creation_date = models.DateTimeField('Date the order was made')
    order_status = models.CharField(max_length=1, choices=ORDER_STATUS, default=CREATED)

    def __unicode__(self):
        return "Order " + str(self.order_number)

    def to_csv(self):
        values = [self.order_id,
                  self.reserved_for,
                  self.paid_for,
                  self.shipped,
                  self.ship_to,
                  self.order_number,
                  self.creation_date]
        return to_csv_from_array(values)

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
        values = [self.order_for.order_id,
                  self.box.box_id,
                  self.cost]
        return to_csv_from_array(values)
