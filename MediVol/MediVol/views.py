from django.contrib import auth
from django.contrib.auth.views import login
from django.http import HttpResponseRedirect
from django.shortcuts import render

def custom_login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/administration/redirect')
    else:
        return login(request)
