from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group

from administration.UserTests import UserTests
from inventory.models import Warehouse
from catalog.models import Category, BoxName
from administration.models import ResetCode

@login_required
def redirect(request):
    user_group = request.user.groups.all()[0].name

    if user_group == 'Admin':
        return HttpResponseRedirect('/inventory')
    elif user_group == 'Box Transfer':
        return HttpResponseRedirect('/inventory')
    if user_group == 'Guest':
        return HttpResponseRedirect('/inventory/create')
    if user_group == 'Read Only':
        return HttpResponseRedirect('/inventory')

@login_required
@user_passes_test(UserTests.user_is_admin, login_url='/administration/forbidden')
def main_page(request):
    return render(request, 'administration/index.html')

def access_forbidden(request):
    return render(request, 'administration/forbidden.html')

@login_required
@user_passes_test(UserTests.user_is_admin, login_url='/administration/forbidden')
def manage_users(request):
    context = {
        'users': User.objects.all().order_by('username'),
        'groups': Group.objects.all().order_by('name'),
        'reset_url': request.build_absolute_uri('/administration/reset_password')
    }

    return render(request, 'administration/manage_users.html', context)

@login_required
@user_passes_test(UserTests.user_is_admin, login_url='/administration/forbidden')
def manage_backups(request):
    return render(request, 'administration/manage_backups.html')

@login_required
@user_passes_test(UserTests.user_is_admin, login_url='/administration/forbidden')
def manage_warehouses(request):
    context = { 'warehouses': Warehouse.objects.all() }

    return render(request, 'administration/manage_warehouses.html', context)

@login_required
@user_passes_test(UserTests.user_is_admin, login_url='/administration/forbidden')
def manage_categories(request):
    context = { 'categories': Category.objects.all() }

    return render(request, 'administration/manage_categories.html', context)

@login_required
@user_passes_test(UserTests.user_is_admin, login_url='/administration/forbidden')
def manage_box_names(request):
    context = { 'box_names': BoxName.objects.all(), 'categories': Category.objects.all() }

    return render(request, 'administration/manage_box_names.html', context)

def reset_password(request, reset_code):
    # if a user is logged in, log them out then reload the page
    if request.user.is_authenticated():
        auth.logout(request)
        return HttpResponseRedirect('/administration/reset_password/' + reset_code)

    context = { 'reset_code': ResetCode.objects.get(code=reset_code) }

    return render(request, 'administration/reset_password.html', context)

def send_reset(request):
    context = { 'reset_url': request.build_absolute_uri('/administration/reset_password') }

    return render(request, 'administration/send_reset.html', context)

@login_required
def user_settings(request):
    context = { 'email': request.user.email, 'reset_url': request.build_absolute_uri('/administration/reset_password') }

    return render(request, 'administration/user_settings.html', context)

@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/login')
