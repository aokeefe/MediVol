from django.conf.urls import patterns, url

from catalog.views import ItemsListView
from catalog import views

urlpatterns = patterns('',
    url(r'^$', ItemsListView.as_view(), name='item-list'),
    url(r'^item_info/(?P<item_id>\w+)/$', views.item_info, name='item_info')
)
