from django.shortcuts import render

from catalog.models import Category, BoxName, Item
from inventory.models import Box, Contents
from orders.models import Order, OrderBox

def catalog(request):
    categories = Category.objects.all()
    categoryStrings = []

    for category in categories:
        categoryStrings.append(category.name)

    context = { 'categories': sorted(categoryStrings) }

    return render(request, 'catalog/catalog.html', context)
    #
    # model = Category
    #
    # def get_context_data(self,**kwargs):
    #     context = super(ItemsListView, self).get_context_data(**kwargs)
    #     context['now'] = timezone.now()
    #     return context

def item_info(request, item_id):
    try:
        item = Item.objects.get(id=item_id)
    except Item.DoesNotExist:
        item = False

    boxes_with_item = False
    orders_with_item = False

    if item:
        contents = Contents.objects.filter(item=item)

        if len(contents) > 0:
            boxes_with_item = []
            for content in contents:
                boxes_with_item.append(content.box_within)

            for box in boxes_with_item:
                order_boxes = OrderBox.objects.filter(box=box)

                if len(order_boxes) > 0:
                    orders_with_item = []
                    for order_box in order_boxes:
                        orders_with_item.append(order_box.order_for)

    context = { 'item': item, 'boxes_with_item': boxes_with_item, 'orders_with_item': orders_with_item }

    return render(request, 'catalog/item_info.html', context)
