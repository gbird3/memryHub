from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django import forms
from django.forms import ModelForm

from django.core.mail import send_mail
from django.template import loader
#
from ..models import Timeline, Memory, File
from home.models import UserInfo
from ..gdrive import createFolder, changeFileData, getAccessToken

@login_required(login_url='/login')
def timelines(request):
    '''View all Timelines'''
    timelines = Timeline.objects.filter(owner=request.user, active=1).order_by('name')
    return render(request, 'timeline.html', {'timelines': timelines})

@login_required(login_url='/login')
def api_create_timeline(request):
    if request.method == 'POST':
        # First check if a root folder (MemryHub) has been created. If not create it.
        try:
            uinfo = UserInfo.objects.get(user=request.user)
        except:
            data = createFolder(request.user, 'MemryHub')

            uinfo = UserInfo()
            uinfo.user = request.user
            uinfo.root_folder_id = data['id']
            uinfo.save()

        data = createFolder(request.user, request.POST.__getitem__('name'), uinfo.root_folder_id)

        t = Timeline()
        t.owner = request.user
        t.name = request.POST.__getitem__('name')
        t.timeline_folder_id = data['id']
        t.save()

        return HttpResponse(t.id)

@login_required(login_url='/login')
def edit_timeline(request, timeline_id):
    access_token = getAccessToken(request.user)

    t = get_object_or_404(Timeline, pk=timeline_id)

    data = {
        'name': t.name,
        'picture': t.image,
        'title': t.image_title
    }

    form = CreateTimelineForm(initial=data)

    if request.method == 'POST':
        form = CreateTimelineForm(request.POST)
        if form.is_valid():
            t = Timeline.objects.get(pk=timeline_id)

            response = changeFileData(request.user, t.timeline_folder_id, form.cleaned_data.get('name'), form.cleaned_data.get('description'))

            t.owner = request.user
            t.name = form.cleaned_data.get('name')
            t.description = form.cleaned_data.get('description')
            t.image = form.cleaned_data.get('picture')
            t.image_title = form.cleaned_data.get('title')
            t.save()

            timeline_id  = t.id

            return HttpResponseRedirect('/timeline/view/{}'.format(timeline_id))

    template_vars = {
        'form': form,
        'parent_id': t.timeline_folder_id,
        'access_token': access_token
    }

    return render(request, 'create.html', template_vars)

class CreateTimelineForm(forms.Form):
    name = forms.CharField(label='Person Name', required=True, max_length=100, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Person Name'}))
    description = forms.CharField(label='Description of Timeline', required=False, max_length=500, widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Short description of your timeline.'}))
    title = forms.CharField(label='Image', required=False, max_length=300, widget=forms.TextInput(attrs={'class': 'form-control'}))
    picture = forms.CharField(required=False, max_length=100, widget=forms.HiddenInput())


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

def testEmail(request):
    # send_mail('Subject here', 'Here is the message.', 'from@example.com', ['to@example.com'], fail_silently=False)

    html_message = loader.render_to_string(
            '../templates/email.html',
            {
                'user': request.user.get_full_name(),
                'memory': 'Test Memory'
            }
        )

    send_mail('Test Email', 'Test wants to share a memory with you on MemryHub. Sign up now', 'support@memryhub.com', ['gregbird12@gmail.com'], fail_silently=False, html_message=html_message)

    return render(request, 'email.html', )
