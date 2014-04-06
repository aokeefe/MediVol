from django.conf.urls import patterns, url
from orders.views import *

urlpatterns = patterns ('',
    #Orders Main Page
    url(r'^$', orders_home),
    url(r'^create/$', create_order),
    url(r'^create/(?P<order_id>\w+)/$', create_order),
    url(r'^create/(?P<order_id>\w+)/(?P<step_num>\d{1})/$', create_order),
    url(r'^create/(?P<order_id>\w+)/(?P<step_num>\d{1})/(?P<box_to_add>\w+)/$', create_order),
    url(r'^review/(?P<orderid>\w+)/$', order_review, name='review_order')
)
