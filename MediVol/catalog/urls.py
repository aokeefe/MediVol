from django.conf.urls import patterns, url

from catalog.views import ItemsListView

urlpatterns = patterns('',
    url(r'^$', ItemsListView.as_view(), name='item-list'),
)