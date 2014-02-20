from django.conf.urls import patterns, url
from orders.views import *

urlpatterns = patterns ('', 
    #Orders Main Page 
    url(r'^create/$', orders_main), 
    url(r'^review/(?P<orderid>\w+)/$', order_review, name='review_order')
)
