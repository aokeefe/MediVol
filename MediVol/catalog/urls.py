from django.conf.urls import patterns, url

from catalog import views

urlpatterns = patterns('',
    url(r'^$', views.catalog, name='catalog'),
    url(r'^item_info/(?P<item_id>\w+)/$', views.item_info, name='item_info')
)
