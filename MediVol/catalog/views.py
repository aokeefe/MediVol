from django.views.generic.list import ListView
from django.utils import timezone
from django.shortcuts import render

from catalog.models import Category
from catalog.models import BoxName
from catalog.models import Item

class ItemsListView(ListView):

    model = Category

    def get_context_data(self,**kwargs):
        context = super(ItemsListView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

def item_info(request, item_id):
    context = { 'item': Item.objects.get(id=item_id) }

    return render(request, 'catalog/item_info.html', context)
