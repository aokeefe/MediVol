from haystack.query import SearchQuerySet
from catalog.models import Category, BoxName, Item

class Searcher:
    @classmethod
    def get_box_names(self, category_name):
        category = Category.objects.get(name=category_name)
        box_names = BoxName.objects.filter(category=category)
        
        box_names_array = []
        
        for box_name in box_names:
            box_names_array.append(box_name.name)
        
        return sorted(box_names_array)
    
    @classmethod
    def get_items(self, box_name):
        box_name = BoxName.objects.get(name=box_name)
        items = Item.objects.filter(box_name=box_name)
        
        items_array = []
        
        for item in items:
            items_array.append(item.name)
        
        return sorted(items_array)
    
    @classmethod
    def search_catalog(self, query, *models):
        results_array = []
        
        if len(models) == 0:
            models = [ Item, BoxName, Category ]
        
        results = SearchQuerySet().autocomplete(name_auto=query).models(*models)
        
        for result in results:
            result = result.object
            results_array.append(result.get_search_results_string())
        
        return results_array