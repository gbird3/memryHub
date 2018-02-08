from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django import forms
from django.forms import ModelForm

from ..models import Timeline, Memory, File

@login_required(login_url='/login')
def add_memory(request, timeline_id):
    form = UserAddsMemoryForm()

    user = request.user
    timeline = get_object_or_404(Timeline, pk=timeline_id)

    social = user.social_auth.get(provider='google-oauth2')
    access_token = social.extra_data['access_token']

    if request.method == 'POST':
        timeline = get_object_or_404(Timeline, pk=timeline_id)

        form = UserAddsMemoryForm(request.POST)

        if form.is_valid():
            m = Memory()

            m.timeline_id = timeline
            m.day = form.cleaned_data.get('start_day')
            m.month = form.cleaned_data.get('start_month')
            m.year = form.cleaned_data.get('start_year')
            m.name = form.cleaned_data.get('memory_name')
            m.description = form.cleaned_data.get('memory_description')
            m.owner = request.user
            m.save()

            if (form.cleaned_data.get('file_id') != ''):
                f = File()
                f.memory = m
                f.name = form.cleaned_data.get('file_name')
                f.description = form.cleaned_data.get('file_description')
                f.file_id = form.cleaned_data.get('file_id')
                f.file_type = form.cleaned_data.get('file_type')
                f.save()

        return HttpResponseRedirect('/timeline/view/{}'.format(timeline_id))

    template_vars = {
        'form': form,
        'access_token': access_token,
        'parent_id': timeline.timeline_folder_id
    }
    return render(request, 'add_memory.html', template_vars)

class UserAddsMemoryForm(forms.Form):
    memory_name = forms.CharField(label='Memory Name', required=True, max_length=100, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Memory Name'}))
    memory_description = forms.CharField(label='Description of your Memory', required=False, max_length=100, widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Short description of your memory.'}))
    start_day = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class':'form-control','placeholder':'Day'}))
    start_month = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class':'form-control','placeholder':'Month'}))
    start_year = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control','placeholder':'Year'}))
    file_id = forms.CharField(required=False, widget=forms.HiddenInput(attrs={'id': 'file_id'}))
    file_name = forms.CharField(required=False, widget=forms.HiddenInput(attrs={'id': 'file_name'}))
    file_description = forms.CharField(required=False, widget=forms.HiddenInput(attrs={'id': 'file_description'}))
    file_type = forms.CharField(required=False, widget=forms.HiddenInput(attrs={'id': 'file_type'}))

def edit_memory(request, memory_id):
    memory = get_object_or_404(Memory, pk=memory_id)

    data = {
        'name': memory.name,
        'day': memory.day,
        'month': memory.month,
        'year': memory.year,
        'description': memory.description
    }

    form = MemoryForm(initial=data)

    if request.method == 'POST':
        form = MemoryForm(request.POST)

        if form.has_changed():
            if form.is_valid():
                m = Memory.objects.get(pk=memory_id)

                m.day = form.cleaned_data.get('day')
                m.month = form.cleaned_data.get('month')
                m.year = form.cleaned_data.get('year')
                m.name = form.cleaned_data.get('name')
                m.description = form.cleaned_data.get('description')
                m.save()

                timeline = m.timeline_id

        return HttpResponseRedirect('/timeline/view/{}'.format(timeline.id))

    return render(request, 'edit_memory.html', {'form': form})

class MemoryForm(ModelForm):
    class Meta:
        model = Memory
        fields = ['day', 'month', 'year', 'name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control','placeholder':'Memory Name'}),
            'description': forms.Textarea(attrs={'class':'form-control','placeholder':'Description of the Memory.'}),
            'day': forms.Select(attrs={'class': 'form-control'}),
            'month': forms.Select(attrs={'class': 'form-control'}),
            'year': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Memory Name',
            'day': 'Day',
            'month': 'Month',
            'year': 'Year'
        }
