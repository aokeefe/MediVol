from django.db import models
import uuid
from inventory.models import Box
from import_export.to_csv import to_csv_from_array, to_array_from_csv
from MediVol import id_generator

ORDER_number_LENGTH = 5

class Customer(models.Model):
    contact_id = models.CharField(max_length=40, unique=True)
    contact_name = models.CharField(max_length=80, unique=False)
    contact_email = models.CharField(max_length=80)
    business_name = models.CharField(max_length=80)
    business_address = models.CharField(max_length=200, null=True)

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

    def save(self, *args, **kwargs):
        if self.contact_id is None: 
            self.contact_id=str(uuid.uuid4())
        elif self.contact_id == '':
            self.contact_id=str(uuid.uuid4())
        super(Customer, self).save(*args, **kwargs)

    def get_search_results_string(self):
        return self.contact_name + ' (' + self.business_name + ')'

    class Meta:
        unique_together=('contact_name', 'business_name')

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer)
    address = models.CharField(max_length=200, unique=True)

    def __unicode__(self):
        return address

class Order(models.Model):
    CREATED = 'C'
    UNPAID = 'U'
    PAID = 'P'
    SHIPPED = 'S'
    PAID_DEPOSIT = 'D'
    CANCELLED = 'F'
    ORDER_STATUS = (
        (CREATED, 'Created'),
        (UNPAID, 'Unpaid For'),
        (PAID, 'Paid For'),
        (SHIPPED, 'Shipped Out'),
        (PAID_DEPOSIT, 'Deposit Paid'),
        (CANCELLED, 'Cancelled'),
    )
    order_number = models.CharField(unique=True, max_length=ORDER_number_LENGTH)
    reserved_for = models.ForeignKey(Customer, null=True)
    paid_for = models.BooleanField(default=False)
    shipped = models.BooleanField(default=False)
    ship_to = models.ForeignKey(ShippingAddress, null=True)
    creation_date = models.DateTimeField('Date the order was made')
    order_status = models.CharField(max_length=1, choices=ORDER_STATUS, default=CREATED)
    price = models.FloatField(null=True)

    def __unicode__(self):
        return "Order " + str(self.order_number)

    def to_csv(self):

        if self.reserved_for is not None:
            reservation = self.reserved_for.contact_id
        else:
            reservation = None

        values = [self.order_number,
                  reservation,
                  self.paid_for,
                  self.shipped,
                  self.ship_to.address,
                  self.creation_date,
                  self.order_status]
        return to_csv_from_array(values)

    @classmethod
    def create_from_csv(cls, csv):
        filtered_values = to_array_from_csv(csv)
        order = Order(order_number=filtered_values[0],
                      reserved_for=Customer.objects.get(contact_id=filtered_values[1]),
                      paid_for=filtered_values[2],
                      shipped=filtered_values[3],
                      ship_to=ShippingAddress.objects.get(address=filtered_values[4]),
                      creation_date=filtered_values[5],
                      order_status=filtered_values[6])
        order.save()
        return order

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

    def save(self, *args, **kwargs):
        if self.order_number is None:
            while True:
                self.order_number = id_generator.id_generator(ORDER_number_LENGTH)
                if not Order.objects.filter(order_number=self.order_number).exists():
                    break

        super(Order, self).save(*args, **kwargs)

class OrderBox(models.Model):
    order_for = models.ForeignKey(Order)
    box = models.ForeignKey(Box)
    cost = models.FloatField(default=0.0)

    def __unicode__(self):
        return str(self.box) + " in order " + str(self.order_for)

    def to_csv(self):
        values = [self.order_for.order_number,
                  self.box.box_id,
                  self.cost]
        return to_csv_from_array(values)

    @classmethod
    def create_from_csv(cls, csv):
        filtered_values = to_array_from_csv(csv)
        order_box = OrderBox(order_for=Order.objects.get(order_number=filtered_values[0]),
                             box=Box.objects.get(box_id=filtered_values[1]),
                             cost=filtered_values[2])
        order_box.save()
        return order_box
