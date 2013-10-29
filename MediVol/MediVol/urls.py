from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from dajaxice.core import dajaxice_autodiscover, dajaxice_config

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
    url(r'^login/$', 'django.contrib.auth.views.login'),
    
    #Routing for Logout
    url(r'^logout/$', 'administration.views.logout'), 

    #Routing for Administration Main Page 
    url(r'^administration/', include('administration.urls')),
)
