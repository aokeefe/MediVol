from django.conf.urls import patterns, url

from inventory import views

urlpatterns = patterns('',
    url(r'^create/$', views.create, name='create'),
    url(r'^create/(?P<order_id>\w+)/$', views.create, name='create'),
    url(r'^view_box_info/(?P<boxid>\w+)/$', views.box_info, name='box_info'),
    url(r'^view_box_info/barcode/(?P<barcodeid>\w+)/$', views.barcode_box_info, name='box_info'),
)
