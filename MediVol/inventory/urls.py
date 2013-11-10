from django.conf.urls import patterns, url

from inventory import views

urlpatterns = patterns('',
    url(r'^create/$', views.create, name='create'),
    url(r'^view_box_info/(?P<boxid>\w+)/$', views.box_info, name='box_info'),
)
