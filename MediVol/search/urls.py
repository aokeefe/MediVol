from django.conf.urls import patterns, url

from search import views

urlpatterns = patterns('',
    url(r'^$', views.search),
    url(r'^(?P<query>\w+)/$', views.search, name='search'),
)