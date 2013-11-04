from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required, user_passes_test

def not_in_guest_group(user): 
    if user: 
        return user.groups.filter(name='guest').count() == 0 
    return False

@login_required
@user_passes_test(not_in_guest_group, login_url='/administration/forbidden') 
def main_page(request):
    return render_to_response('administration/index.html')

def access_forbidden(request): 
    return render_to_response('administration/forbidden.html')

#Logout View
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/login')
