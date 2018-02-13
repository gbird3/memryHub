from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django import forms
from django.forms import ModelForm

import json

from ..models import Timeline, Memory, File
from ..gdrive import createFolder

class UserAddsMemoryForm(forms.Form):
    memory_name = forms.CharField(label='Memory Name', required=True, max_length=100, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Memory Name'}))
    memory_description = forms.CharField(label='Description of your Memory', required=False, max_length=100, widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Short description of your memory.'}))
    start_day = forms.IntegerField(label='Day', required=False, widget=forms.NumberInput(attrs={'class':'form-control','placeholder':'Day'}))
    start_month = forms.IntegerField(label='Month', required=False, widget=forms.NumberInput(attrs={'class':'form-control','placeholder':'Month'}))
    start_year = forms.IntegerField(label='Year', widget=forms.NumberInput(attrs={'class':'form-control','placeholder':'Year'}))
    city = forms.CharField(label='City', required=False, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}))
    state = forms.CharField(label='State', required=False, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}))
    country = forms.CharField(label='Country', required=False, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}))

@login_required(login_url='/login')
def api_add_memory(request):
    if request.method == 'POST':
        timeline = get_object_or_404(Timeline, pk=request.POST.__getitem__('timeline'))

        data = createFolder(request.user, request.POST.__getitem__('name'), timeline.timeline_folder_id)

        m = Memory()
        m.name = request.POST.__getitem__('name')
        m.year = request.POST.__getitem__('year')
        m.owner = request.user
        m.folder_id = data['id']
        m.timeline_id = timeline

        m.save()

    return HttpResponse(m.id)

@login_required(login_url='/login')
def attach_files(request, memory_id):
    user = request.user
    memory = get_object_or_404(Memory, pk=memory_id)
    timeline = get_object_or_404(Timeline, pk=memory.timeline_id.id)

    social = user.social_auth.get(provider='google-oauth2')
    access_token = social.extra_data['access_token']

    data = {
        'memory_name': memory.name,
        'start_day': memory.day,
        'start_month': memory.month,
        'start_year': memory.year,
        'memory_description': memory.description
    }

    form = UserAddsMemoryForm(initial=data)

    if request.method == 'POST':
        form = MemoryForm(request.POST)

        if form.has_changed():
            if form.is_valid():
                m = Memory.objects.get(pk=memory_id)

                m.day = form.cleaned_data.get('start_day')
                m.month = form.cleaned_data.get('start_month')
                m.year = form.cleaned_data.get('start_year')
                m.name = form.cleaned_data.get('memory_name')
                m.description = form.cleaned_data.get('memory_description')
                m.save()

                timeline = m.timeline_id

        return HttpResponseRedirect('/timeline/view/{}'.format(timeline.id))


    template_vars = {
        'form': form,
        'access_token': access_token,
        'parent_id': memory.folder_id,
        'memory_id': memory.id,
        'timeline_id': timeline.id
    }
    return render(request, 'attach_files.html', template_vars)

@login_required(login_url='/login')
def api_attach_file(request):
    if request.method == 'POST':
        memory = get_object_or_404(Memory, pk=request.POST.__getitem__('memory_id'))
        f = File()
        f.memory = memory
        f.name = request.POST.__getitem__('name')
        f.description = request.POST.__getitem__('description')
        f.file_id = request.POST.__getitem__('id')
        f.file_type = request.POST.__getitem__('type')
        f.save()

    return HttpResponse(200)


@login_required(login_url='/login')
def delete_memory(request, memory_id):
    m = Memory.objects.get(pk=memory_id)
    m.active = 0
    m.save()

    f = File.objects.filter(memory_id=memory_id).update(active=0)


    timeline = m.timeline_id

    return HttpResponseRedirect('/timeline/view/{}'.format(timeline.id))

@login_required(login_url='/login')
def delete_file(request, file_id):
    f = File.objects.get(pk=file_id)
    f.active = 0
    f.save()

    memory = f.memory

    timeline = Memory.objects.get(pk=memory.id).timeline_id

    return HttpResponseRedirect('/timeline/view/{}'.format(timeline.id))
