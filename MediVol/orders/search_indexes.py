from haystack import indexes
from orders.models import Customer, Order, OrderBox

class CustomerIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    contact_name = indexes.CharField(model_attr='contact_name')
    contact_email = indexes.CharField(model_attr='contact_email')
    business_name = indexes.CharField(model_attr='business_name')
    business_address = indexes.CharField(model_attr='business_address')

    content_auto = indexes.EdgeNgramField(use_template=True)

    def get_model(self):
        return Customer

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
