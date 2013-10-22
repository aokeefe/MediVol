from django.conf.urls import *
from administration.views import *

urlpatterns = patterns ('',
  #Administration Main Page
  url(r'^$', main_page),

  #Administration Forbidden Page 
  url(r'^forbidden/', access_forbidden),
)
