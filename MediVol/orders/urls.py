from django.conf.urls import patterns, url
from orders.views import *

urlpatterns = patterns ('', 
    #Orders Main Page 
    url(r'^$', orders_main), 
)
