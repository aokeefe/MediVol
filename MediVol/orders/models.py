from django.db import models
from inventory.models import Box

class Customer(models.Model):
    contact_name = models.CharField(max_length=80)
    contact_email = models.CharField(max_length=80)
    business_name = models.CharField(max_length=80)
    business_address = models.CharField(max_length=200, null=True)
    shipping_address = models.CharField(max_length=200, null=True)

    def __unicode__(self):
        return "contact info for: " + self.business_name

    def get_search_results_string(self):
        return self.contact_name + ' (' + self.business_name + ')'

    class Meta:
        unique_together=('contact_name', 'business_name')

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
    reserved_for = models.ForeignKey(Customer, null=True)
    paid_for = models.BooleanField(default=False)
    shipped = models.BooleanField(default=False)
    ship_to = models.CharField(max_length=300, null=True)
    order_number = models.IntegerField()
    creation_date = models.DateTimeField('Date the order was made')
    order_status = models.CharField(max_length=1, choices=ORDER_STATUS, default=CREATED)
    price = models.FloatField(null=True)

    def __unicode__(self):
        return "Order " + str(self.order_number)
    #def to_csv(self):
        #TODO
    def get_weight(self):
        order_weight = 0.0
        for order_box in self.orderbox_set.all():
            order_weight = float(order_weight) + float(order_box.box.weight)
        return ("%.1f" % order_weight)

    def get_cost(self):
        order_cost = 0.0
        for order_box in self.orderbox_set.all():
            order_cost = float(order_cost) + float(order_box.cost)
        return ("%.2f" % order_cost)

    def get_creation_date_display(self):
        creation_date = str(self.creation_date).split(' ')[0]
        creation_array = creation_date.split('-')
        return creation_array[1] + '/' + creation_array[2] + '/' + creation_array[0]

class OrderBox(models.Model):
    order_for = models.ForeignKey(Order)
    box = models.ForeignKey(Box)
    cost = models.FloatField(default=0.0)

    def __unicode__(self):
        return self.box + " in order " + self.order_for

    def to_csv(self):
        return self.order_for.order_number + ", " + self.box.box_id
