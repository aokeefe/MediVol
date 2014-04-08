from haystack import indexes
from inventory.models import Box, Contents

class BoxIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    box_id = indexes.CharField(model_attr='box_id')
    barcode = indexes.CharField(model_attr='barcode')

    content_auto = indexes.EdgeNgramField(use_template=True)

    def get_model(self):
        return Box

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

class ContentsIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    # TODO: fix this
    # expiration = indexes.DateTimeField(model_attr='expiration', null=True)

    content_auto = indexes.EdgeNgramField(use_template=True)

    def get_model(self):
        return Contents

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
