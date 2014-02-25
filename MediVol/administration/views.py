from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group

from administration.models import Warehouse

def user_is_admin(user): 
    if user.is_authenticated():
        return user.groups.all()[0].name == 'Admin'
    return False

@login_required
@user_passes_test(user_is_admin, login_url='/administration/forbidden')
def main_page(request):
    return render(request, 'administration/index.html')

def access_forbidden(request): 
    return render(request, 'administration/forbidden.html')

@login_required
@user_passes_test(user_is_admin, login_url='/administration/forbidden')
def manage_users(request):
    context = { 'users': User.objects.all(), 'groups': Group.objects.all() }

    return render(request, 'administration/manage_users.html', context)

@login_required
@user_passes_test(user_is_admin, login_url='/administration/forbidden')
def manage_backups(request):
    return render(request, 'administration/manage_backups.html')

@login_required
@user_passes_test(user_is_admin, login_url='/administration/forbidden')
def manage_warehouses(request):
    context = { 'warehouses': Warehouse.objects.all() }

    return render(request, 'administration/manage_warehouses.html', context)

#Logout View
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/login')
