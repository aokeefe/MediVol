from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test

from administration.models import Warehouse

def not_in_guest_group(user): 
    if user: 
        return user.groups.filter(name='guest').count() == 0 
    return False

@login_required
@user_passes_test(not_in_guest_group, login_url='/administration/forbidden') 
def main_page(request):
    return render(request, 'administration/index.html')

def access_forbidden(request): 
    return render(request, 'administration/forbidden.html')

def manage_users(request):
    return render(request, 'administration/manage_users.html')

def manage_backups(request):
    return render(request, 'administration/manage_backups.html')

def manage_warehouses(request):
    context = { 'warehouses': Warehouse.objects.all() }

    return render(request, 'administration/manage_warehouses.html', context)

#Logout View
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/login')
