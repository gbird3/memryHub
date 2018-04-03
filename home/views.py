from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User

from .models import Group, UserHasGroup

def index(request):
    user = request.user

    template_vars = {
        'user': user,
    }
    return render(request, 'index.html',template_vars)

def logout(request):
    """Logs out a user"""
    auth_logout(request)
    return render_to_response('index.html')

def login(request):
    return render(request, 'login.html')


class CreateGroupForm(forms.Form):
    name = forms.CharField(label='Group Name', required=True, max_length=100, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Group Name'}))

def groups(request):
    form = CreateGroupForm()

    groups = Group.objects.filter(owner=request.user)

    if request.method == 'POST':
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            g = Group()
            g.owner = request.user
            g.name = form.cleaned_data.get('name')
            g.save()

        return HttpResponseRedirect('/groups')

    template_vars = {
        'groups': groups,
        'form': form
    }

    return render(request, 'groups.html', template_vars)

class AddUserToGroupForm(forms.Form):
    email = forms.CharField(label='User Email', required=True, max_length=300, widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email'}))

def group_users(request, group_id):
    group = Group.objects.get(id=group_id)
    form = AddUserToGroupForm()
    users = UserHasGroup.objects.filter(group=group)

    if request.method == 'POST':
        form = AddUserToGroupForm(request.POST)
        if form.is_valid():

            user = User.objects.get(email=form.cleaned_data.get('email'))
            if user:
                gu = UserHasGroup()
                gu.group = group
                gu.user = user
                gu.save()

    template_vars = {
        'form': form,
        'group': group,
        'users': users
    }

    return render(request, 'group-users.html', template_vars)