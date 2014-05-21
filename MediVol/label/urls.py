from django.conf.urls import patterns, url

from label import views

urlpatterns = patterns('', 
  url(r'^create/(?P<box_barcode>\w+)/$', views.create_label, name='create'),
)
