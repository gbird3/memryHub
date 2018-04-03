from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django import forms
from django.forms import ModelForm

from datetime import datetime
from django.core.mail import send_mail
from django.template import loader

from ..models import Timeline, Memory, File, SharedTimeline, GroupHasTimeline
from home.models import UserInfo, Group, UserHasGroup
from ..gdrive import createFolder, changeFileData, getAccessToken, shareWithUser, updateSharing

@login_required(login_url='/login')
def timelines(request):
    '''View all Timelines'''
    timelines = Timeline.objects.filter(owner=request.user, active=1).order_by('name')
    shared_timelines = SharedTimeline.objects.filter(user=request.user, active=1)

    timeline_count = timelines.count()
    return render(request, 'timeline.html', {'timelines': timelines,'timeline_count':timeline_count, 'shared_timelines': shared_timelines})

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
        'title': t.image_title,
        'timeline_id':timeline_id
    }

    form = CreateTimelineForm(initial=data)

    if request.method == 'POST':
        form = CreateTimelineForm(request.POST)
        if form.is_valid():
            t = Timeline.objects.get(pk=timeline_id)

            changeFileData(request.user, t.timeline_folder_id, form.cleaned_data.get('name'), form.cleaned_data.get('description'))

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
        'access_token': access_token,
        'timeline_id':timeline_id
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
    can_edit = False
    if timeline.owner == request.user:
        can_edit = True
    else:
        shared_timeline = SharedTimeline.objects.get(timeline=timeline, user=request.user)
        if shared_timeline.permission == 'writer':
            can_edit = True

    memories = Memory.objects.filter(timeline_id=timeline_id, active=1).order_by('year')
    files = File.objects.filter(memory__in = memories, active=1)

    access_token = getAccessToken(request.user)

    date_dict = {}

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
#            if hasattr(e,'year'):
#                my_time = '00:00'
#                if e.day is None:
#                    my_day = '01'
#                    my_time = '2:01'
#                else:
#                    my_day = str(e.day)
#
#                if e.month is None:
#                    my_month = '01'
#                    my_time = '2:02'
#                else:
#                    my_month = str(e.month)
#
#                if e.year is None:
#                    my_year = '1900'
#                    my_time = '2:03'
#                else:
#                    my_year = str(e.year)
#                date_dict[e.id] = datetime.strptime(my_year + ' ' + my_month + ' ' + my_day + ' ' + my_time, '%Y %m %d %H:%M')
#                print('++++++++++++++++++++++++++++++++++++++',date_dict)
            if hasattr(e,'year'):
                if e.year >= temp_year:
                    temp_divider = Divider_Object()
                    temp_divider.divider_year = temp_year
                    memories_with_years.insert(temp_position,temp_divider)
                    temp_year = temp_year + 10
                if e.month == 1:
                    e.month = "January"
                elif e.month == 2:
                    e.month = "February"
                elif e.month == 3:
                    e.month = "March"
                elif e.month == 4:
                    e.month = "April"
                elif e.month == 5:
                    e.month = "May"
                elif e.month == 6:
                    e.month = "June"
                elif e.month == 7:
                    e.month = "July"
                elif e.month == 8:
                    e.month = "August"
                elif e.month == 9:
                    e.month = "September"
                elif e.month == 10:
                    e.month = "October"
                elif e.month == 11:
                    e.month = "November"
                elif e.month == 12:
                    e.month = "December"
                else:
                    e.month = None
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

    memory_count = memories.count()

    template_vars = {
        'timeline': timeline,
        'can_edit': can_edit,
        'memories': memories,
        'files': files,
        'first_year': first_year,
        'last_year': last_year,
        'memories_with_years': memories_with_years,
        'memory_count': memory_count,
        'date_dict':date_dict,
        'access_token': access_token
    }

    return render(request, 'view.html', template_vars)

@login_required(login_url='/login')
def delete(request, timeline_id):
    '''Delete a timeline'''
    t = Timeline.objects.get(pk=timeline_id)
    t.active = 0
    t.save()

    SharedTimeline.objects.filter(timeline=t).update(active=0)

    return HttpResponseRedirect('/timeline')

@login_required(login_url='/login')
def timeline_sharing(request, timeline_id):
    timeline = get_object_or_404(Timeline, pk=timeline_id)
    users = SharedTimeline.objects.filter(timeline=timeline)
    user_groups = Group.objects.filter(owner=request.user)
    groups = GroupHasTimeline.objects.filter(timeline=timeline)

    if request.method == 'POST':
        form = request.POST
        group = get_object_or_404(Group, pk=form['user_group_id'])
        users_in_group = UserHasGroup.objects.filter(group=group)

        for user in users_in_group:
            share_timeline(request.user, user.user.email, timeline, form['permission'])
        
        if GroupHasTimeline.objects.filter(group=group, timeline=timeline).exists():
            gt = GroupHasTimeline.objects.get(group=group, timeline=timeline)
        else: 
            gt = GroupHasTimeline()

        gt.group = group
        gt.timeline = timeline
        gt.permission = form['permission']
        gt.save()

        return HttpResponseRedirect('/timeline/sharing/{}/'.format(timeline.id))
        
    template_vars = {
        'timeline': timeline,
        'users': users,
        'user_groups': user_groups,
        'groups': groups
    }

    return render(request, 'sharing.html', template_vars)

@login_required(login_url='/login')
def api_share_timeline(request):
    '''
        Share Timeline with user
        Returns status code
           200 Timeline Shared
           201 User doesn't exist, sent invite email
           400 Error Sharing from Google Drive
    '''
    if request.method == 'POST':
        email = request.POST.__getitem__('email')
        role = request.POST.__getitem__('access')

        if User.objects.filter(email=email).exists():
            timeline = Timeline.objects.get(pk=request.POST.__getitem__('timeline'))

            status = share_timeline(request.user, email, timeline, role)
        else:
            html_message = loader.render_to_string(
                    '../templates/email.html',
                    {
                        'user': request.user.get_full_name()
                    }
            )

            send_mail('MemryHub Invite', '{} wants to share a Timeline with you on MemryHub. Sign up at memryhub.com'.format(request.user.get_full_name()), 'memryhub@memryhub.com', [email], fail_silently=False, html_message=html_message)

            status = 201

    return HttpResponse(status)

def share_timeline(owner, email, timeline, role):
     # Share the folder with the user
    response = shareWithUser(owner, email, timeline.timeline_folder_id, role)
    status = 400
    data = response.json()

    user = User.objects.get(email=email)

    # If the sharing was a success, add the user to the shared DB or update that users permissions
    if response.status_code == 200:
        if SharedTimeline.objects.filter(user=user, timeline=timeline).exists():
            s = SharedTimeline.objects.get(user=user, timeline=timeline)
            s.permission = role
            s.permission_id = data['id']
            s.save()
        else:
            s = SharedTimeline()
            s.user = user
            s.timeline = timeline
            s.permission = role
            s.permission_id = data['id']
            s.save()

        status = response.status_code
    return status

@login_required(login_url='/login')
def api_update_share_timeline(request):
    '''
        Update Sharing Preferences
        Returns status code
          200 Sharing Settings updated
          400 Error Sharing from Google Drive
    '''
    if request.method == 'POST':
        shared_id = request.POST.__getitem__('id')
        role = request.POST.__getitem__('access')

        shared = SharedTimeline.objects.get(pk=shared_id)

        # Share the folder with the user
        response = updateSharing(request.user, shared.permission_id, shared.timeline.timeline_folder_id, role)
        status = 400

        # If the sharing was a success, add the user to the shared DB or update that users permissions
        if response.status_code == 200:
            s = SharedTimeline.objects.get(pk=shared_id)
            s.permission = role
            s.save()

            status = response.status_code

    return HttpResponse(status)

@login_required(login_url='/login')
def testEmail(request):
    # send_mail('Subject here', 'Here is the message.', 'from@example.com', ['to@example.com'], fail_silently=False)

    html_message = loader.render_to_string(
            '../templates/email.html',
            {
                'user': request.user.get_full_name(),
                'memory': 'Test Memory'
            }
        )

    send_mail('Test Email', 'Test wants to share a memory with you on MemryHub. Sign up now', 'memryhub@memryhub.com', ['gregbird12@gmail.com'], fail_silently=False, html_message=html_message)

    return render(request, 'email.html', )
