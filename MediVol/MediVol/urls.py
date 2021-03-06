from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from dajaxice.core import dajaxice_autodiscover, dajaxice_config
from MediVol.views import *

dajaxice_autodiscover()
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'MediVol.views.home', name='home'),
    # url(r'^MediVol/', include('MediVol.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),

    #Routing for Login
    url(r'^$', custom_login),
    url(r'^login/$', custom_login),

    #Routing for Logout
    url(r'^logout/$', 'administration.views.logout'),

    #Routing for Administration Main Page
    url(r'^administration/', include('administration.urls')),

    #Routing for Inventory
    url(r'^inventory/', include('inventory.urls')),

    #Routing for Orders
    url(r'^orders/', include('orders.urls')),

    #Routing for Catalog
    url(r'^catalog/', include('catalog.urls')),

    #Routing for Labels 
    url(r'^label/', include('label.urls')),
)
