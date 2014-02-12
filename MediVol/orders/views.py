from django.shortcuts import render

from catalog.models import Category

#Display the main page of ordering 
def orders_main(request):
    
    categories = Category.objects.all()
    categoryStrings = []

    for category in categories:
        categoryStrings.append(category.name)

    context = { 'categories': sorted(categoryStrings) }

    return render(request, 'orders/orders.html', context)

