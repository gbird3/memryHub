from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django import forms
from django.forms import ModelForm

from ..models import Timeline, Memory, File
from home.models import UserInfo
from ..gdrive import createFolder

@login_required(login_url='/login')
def timelines(request):
    '''View all Timelines'''
    timelines = Timeline.objects.filter(owner=request.user, active=1)
    return render(request, 'timeline.html', {'timelines': timelines})

@login_required(login_url='/login')
def create(request):
    '''Create a timeline'''
    form = CreateTimelineForm()

    # First check if a root folder (MemryHub) has been created. If not create it.
    try:
        uinfo = UserInfo.objects.get(user=request.user)
    except:
        data = createFolder(request.user, 'MemryHub')

        print(data)
        uinfo = UserInfo()
        uinfo.user = request.user
        uinfo.root_folder_id = data['id']
        uinfo.save()


    if request.method == 'POST':
        form = CreateTimelineForm(request.POST)

        if form.is_valid():

            data = createFolder(request.user, form.cleaned_data.get('name'), uinfo.root_folder_id)

            t = Timeline()
            t.owner = request.user
            t.name = form.cleaned_data.get('name')
            t.description = form.cleaned_data.get('description')
            print("+++++++++++++++++++++++++++++++++++++++++",data)
            t.timeline_folder_id = data['id']
            t.save()

            timeline_id  = t.id

        return HttpResponseRedirect('/timeline/view/{}'.format(timeline_id))

    return render(request, 'create.html', {'form': form})

@login_required(login_url='/login')
def edit(request, timeline_id):
    '''Edit an individual timeline'''
    timeline = get_object_or_404(Timeline, pk=timeline_id)

    data = {
        'name': timeline.name,
        'description': timeline.description
    }

    form = CreateTimelineForm(initial=data)

    if request.method == 'POST':

        form = CreateTimelineForm(request.POST)
        if form.is_valid():
            if form.has_changed():
                t = Timeline.objects.get(pk=timeline_id)
                t.name = form.cleaned_data.get('name')
                t.description = form.cleaned_data.get('description')
                t.save()

        return HttpResponseRedirect('/timeline')

    return render(request, 'edit.html', {'form': form})

class CreateTimelineForm(forms.Form):
    name = forms.CharField(label='Person Name', required=True, max_length=100, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Person Name'}))
    description = forms.CharField(label='Description of Timeline', required=False, max_length=100, widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Short description of your timeline.'}))

@login_required(login_url='/login')
def view(request, timeline_id):
    '''View an individual timeline'''
    timeline = get_object_or_404(Timeline, pk=timeline_id)

    memories = Memory.objects.filter(timeline_id=timeline_id, active=1).order_by('year')
    files = File.objects.filter(memory__in = memories, active=1)


    #adding divider years between memories
    if hasattr(memories.first(), 'year'):
        memories_with_years = list(memories)

        first_year_temp = memories.first().year
        first_year_temp = first_year_temp - (first_year_temp % 10)
        temp_year = first_year_temp + 10
        temp_position = 0
        last_year_temp = memories.last().year
        last_year_temp = last_year_temp + (10 - (last_year_temp % 10))

        memories_with_years.insert(0,first_year_temp)

        class Divider_Object:
            divider_year = 0

        temp_divider = Divider_Object()
        temp_divider.divider_year = 2000

        for e in memories_with_years:
            if hasattr(e,'year'):
                if e.year >= temp_year:
                    temp_divider = Divider_Object()
                    temp_divider.divider_year = temp_year
                    memories_with_years.insert(temp_position,temp_divider)
                    temp_year = temp_year + 10
            temp_position = temp_position + 1
    else:
        memories_with_years = list(memories)

    if hasattr(memories.first(), 'year'):
         first_year = memories.first().year
         first_year = first_year - (first_year % 10)

         last_year = memories.last().year
         last_year = last_year + (10 - (last_year % 10))

    else:
        first_year = ""
        last_year = ""

    template_vars = {
        'timeline': timeline,
        'memories': memories,
        'files': files,
        'first_year': first_year,
        'last_year': last_year,
        'memories_with_years': memories_with_years
    }

    return render(request, 'view.html', template_vars)

@login_required(login_url='/login')
def delete(request, timeline_id):
    '''Delete a timeline'''
    t = Timeline.objects.get(pk=timeline_id)
    t.active = 0
    t.save()

    return HttpResponseRedirect('/timeline')
