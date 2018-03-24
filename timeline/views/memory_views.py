from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django import forms
from django.forms import ModelForm

import json

from ..models import Timeline, Memory, File
from ..gdrive import createFolder, changeFileData, getAccessToken

class UserAddsMemoryForm(forms.Form):
    memory_name = forms.CharField(label='Memory Name', required=True, max_length=100, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Memory Name'}))
    memory_description = forms.CharField(label='Description of your Memory', required=False, max_length=100, widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Short description of your memory.'}))
    start_day = forms.IntegerField(label='Day', required=False, widget=forms.NumberInput(attrs={'class':'form-control','placeholder':'Day'}))
    start_month = forms.IntegerField(label='Month', required=False, widget=forms.NumberInput(attrs={'class':'form-control','placeholder':'Month'}))
    start_year = forms.IntegerField(label='Year', widget=forms.NumberInput(attrs={'class':'form-control','placeholder':'Year'}))
    city = forms.CharField(label='City', required=False, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}))
    state = forms.CharField(label='State', required=False, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}))
    country = forms.CharField(label='Country', required=False, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}))
    latitude = forms.DecimalField(label='Latitude', required=False, widget=forms.NumberInput(attrs={'class':'form-control','placeholder:':'Latitude'}))
    longitude = forms.DecimalField(label='Longitude', required=False, widget=forms.NumberInput(attrs={'class':'form-control','placeholder:':'Longitude'}))

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
    memory = get_object_or_404(Memory, pk=memory_id)
    files = File.objects.filter(memory=memory_id, active=1)

    timeline = get_object_or_404(Timeline, pk=memory.timeline_id.id)

    access_token = getAccessToken(request.user)

    data = {
        'memory_name': memory.name,
        'start_day': memory.day,
        'start_month': memory.month,
        'start_year': memory.year,
        'memory_description': memory.description,
        'memory': memory,
        'city': memory.city,
        'state': memory.state,
        'country': memory.country,
        'latitude': memory.latitude,
        'longitude': memory.longitude,

    }

    form = UserAddsMemoryForm(initial=data)

    if request.method == 'POST':
        form = UserAddsMemoryForm(request.POST)

        if form.has_changed():
            if form.is_valid():
                m = Memory.objects.get(pk=memory_id)

                response = changeFileData(request.user, m.folder_id, form.cleaned_data.get('memory_name'), form.cleaned_data.get('memory_description'))
                m.day = form.cleaned_data.get('start_day')
                m.month = form.cleaned_data.get('start_month')
                m.year = form.cleaned_data.get('start_year')
                m.name = form.cleaned_data.get('memory_name')
                m.description = form.cleaned_data.get('memory_description')
                m.city = form.cleaned_data.get('city')
                m.state = form.cleaned_data.get('state')
                m.country = form.cleaned_data.get('country')
                m.latitude = form.cleaned_data.get('latitude')
                m.longitude = form.cleaned_data.get('longitude')
                m.save()

                timeline = m.timeline_id

        return HttpResponseRedirect('/timeline/view/{}'.format(timeline.id))


    template_vars = {
        'form': form,
        'access_token': access_token,
        'parent_id': memory.folder_id,
        'memory_id': memory.id,
        'timeline_id': timeline.id,
        'files': files,
        'memory': memory,
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

        return HttpResponse(f.id)


@login_required(login_url='/login')
def delete_memory(request, memory_id):
    m = Memory.objects.get(pk=memory_id)
    m.active = 0
    m.save()

    f = File.objects.filter(memory_id=memory_id).update(active=0)


    timeline = m.timeline_id

    return HttpResponseRedirect('/timeline/view/{}'.format(timeline.id))
