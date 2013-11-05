from django.shortcuts import render
from Searcher import Searcher

def search(request):
    context = {}
    
    if request.method == 'GET' and 'query' in request.GET:
        context['query'] = request.GET['query']
        searcher = Searcher()
        results = searcher.search(content['query'])
    
    return render(request, 'search/search.html', context)