from django.db import models
from inventory.models import Box
from import_export.to_csv import to_csv_from_array, to_array_from_csv

class Customer(models.Model):
    contact_id = models.IntegerField(unique=True)
    contact_name = models.CharField(max_length=80)
    contact_email = models.CharField(max_length=80)
    business_name = models.CharField(max_length=80)
    business_address = models.CharField(max_length=200, null=True)
    shipping_address = models.CharField(max_length=200)

    def __unicode__(self):
        return "Contact info for: " + self.contact_name + ' at ' + self.business_name

    def to_csv(self):
        values = [self.contact_id,
                  self.contact_name,
                  self.contact_email,
                  self.business_name,
                  self.business_address,
                  self.shipping_address]
        return to_csv_from_array(values)

    @classmethod
    def create_from_csv(cls, csv):
        filtered_values = to_array_from_csv(csv)
        customer = Customer(contact_id=filtered_values[0],
                            contact_name=filtered_values[1],
                            contact_email=filtered_values[2],
                            business_name=filtered_values[3],
                            business_address=filtered_values[4],
                            shipping_address=filtered_values[5])
        customer.save()
        return customer
        
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
    reserved_for = models.ForeignKey(Customer, null=True)
    paid_for = models.BooleanField(default=False)
    order_number = models.IntegerField()
    creation_date = models.DateTimeField('Date the order was made')
    order_status = models.CharField(max_length=1, choices=ORDER_STATUS, default=CREATED)

    def __unicode__(self):
        return "Order " + str(self.order_number)

    def to_csv(self):

        if self.reserved_for is not None:
            reservation = self.reserved_for.customer_id
        else:
            reservation = None

        values = [self.order_id,
                  reservation,
                  self.paid_for,
                  self.order_number,
                  self.creation_date,
                  self.order_status]
        return to_csv_from_array(values)

    @classmethod
    def create_from_csv(cls, csv):
        filtered_values = to_array_from_csv(csv)
        order = Order(order_id=filtered_values[0],
                      reserved_for=Customer.objects.get(customer_id=filtered_values[1]),
                      paid_for=filtered_values[2],
                      order_number=filtered_values[3],
                      creation_date=filtered_values[4],
                      order_status=filtered_values[5])
        order.save()
        return order

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

    @classmethod
    def create_from_csv(cls, csv):
        filtered_values = to_array_from_csv(csv)
        order_box = OrderBox(order_for=Order.objects.get(order_id=filtered_values[0]),
                             box=Box.objects.get(box_id=filtered_values[1]),
                             cost=filtered_values[2])
        order_box.save()
        return order_box
