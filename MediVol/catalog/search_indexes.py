from haystack import indexes
from catalog.models import Item, Category, BoxName

class CategoryIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    letter = indexes.CharField(model_attr='letter')
    name = indexes.CharField(model_attr='name')

    content_auto = indexes.EdgeNgramField(use_template=True)

    def get_model(self):
        return Category

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

class BoxNameIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')

    content_auto = indexes.EdgeNgramField(use_template=True)

    def get_model(self):
        return BoxName

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

class ItemIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')
    description = indexes.CharField(model_attr='description')

    content_auto = indexes.EdgeNgramField(use_template=True)

    def get_model(self):
        return Item

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
