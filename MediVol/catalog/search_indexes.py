from haystack import indexes
from catalog.models import Item, Category, BoxName

class CategoryIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True)
    letter = indexes.CharField(model_attr='letter')
    name = indexes.CharField(model_attr='name')
    
    name_auto = indexes.EdgeNgramField(model_attr='name')
    
    def get_model(self):
        return Category
    
    def index_queryset(self, using=None):
        return self.get_model().objects.all()
        
class BoxNameIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True)
    name = indexes.CharField(model_attr='name')
    
    name_auto = indexes.EdgeNgramField(model_attr='name')
    
    def get_model(self):
        return BoxName
    
    def index_queryset(self, using=None):
        return self.get_model().objects.all()

class ItemIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True)
    name = indexes.CharField(model_attr='name')
    description = indexes.CharField(model_attr='description')
    
    name_auto = indexes.EdgeNgramField(model_attr='name')

    def get_model(self):
        return Item
        
    def index_queryset(self, using=None):
        return self.get_model().objects.all()