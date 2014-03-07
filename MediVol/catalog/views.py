from django.views.generic.list import ListView
from django.utils import timezone

from catalog.models import Category
from catalog.models import BoxName
from catalog.models import Item

class ItemsListView(ListView):
    
    model = Category
    
    def get_context_data(self,**kwargs):
        context = super(ItemsListView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context