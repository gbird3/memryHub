from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django import forms
from django.forms import ModelForm

import requests
import json

from .models import Timeline, Card, Memory, DAY_CHOICES, MONTH_CHOICES, YEAR_CHOICES
from home.models import UserInfo

url = 'https://www.googleapis.com/drive/v3/files'
# Create your views here.

@login_required(login_url='/login')
def timelines(request):

    timelines = Timeline.objects.filter(owner=request.user)

    return render(request, 'timeline.html', {'timelines': timelines})

@login_required(login_url='/login')
def create(request):
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
            t.timeline_folder_id = data['id']
            t.save()

            timeline_id  = t.id

        return HttpResponseRedirect('/timeline/view/{}'.format(timeline_id))

    return render(request, 'create.html', {'form': form})

def createFolder(user, folderName, parents=None):
    social = user.social_auth.get(provider='google-oauth2')
    access_token = social.extra_data['access_token']

    headers = {
        'Authorization':'Bearer {}'.format(access_token),
        'Content-Type': 'application/json'
    }

    file_metadata = {
        'name': folderName,
        'mimeType': 'application/vnd.google-apps.folder',
    }

    if parents:
        file_metadata['parents'] = [parents]

    response = requests.post(
        url,
        headers = headers,
        data = json.dumps(file_metadata)
    )

    return response.json()

@login_required(login_url='/login')
def edit(request, timeline_id):
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
    timeline = get_object_or_404(Timeline, pk=timeline_id)

    cards = Card.objects.filter(timeline_id=timeline_id).order_by('start_year')
    memories = Memory.objects.filter(card__in = cards)

    first_year = cards.first().start_year
    first_year = first_year - (first_year % 10)

    last_year = cards.last().start_year
    last_year = last_year + (10 - (last_year % 10))

    template_vars = {
        'timeline': timeline,
        'cards': cards,
        'memories': memories,
        'first_year': first_year,
        'last_year': last_year
    }

    return render(request, 'view.html', template_vars)


class UserAddsMemoryForm(forms.Form):
    card_name = forms.CharField(label='Memory Name', required=True, max_length=100, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Memory Name'}))
    card_description = forms.CharField(label='Description of your Memory', required=False, max_length=100, widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Short description of your memory.'}))
    start_day = forms.ChoiceField(required=False, choices=((0, 'Day'),) + DAY_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    start_month = forms.ChoiceField(required=False, choices=((0, 'Month'),) + MONTH_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    start_year = forms.ChoiceField(choices=(('', 'Year'),) + YEAR_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    file_id = forms.CharField(required=False, widget=forms.HiddenInput(attrs={'id': 'file_id'}))
    file_name = forms.CharField(required=False, widget=forms.HiddenInput(attrs={'id': 'file_name'}))
    file_description = forms.CharField(required=False, widget=forms.HiddenInput(attrs={'id': 'file_description'}))
    file_type = forms.CharField(required=False, widget=forms.HiddenInput(attrs={'id': 'file_type'}))

@login_required(login_url='/login')
def create_card(request, timeline_id):
    form = UserAddsMemoryForm()

    user = request.user
    timeline = get_object_or_404(Timeline, pk=timeline_id)

    social = user.social_auth.get(provider='google-oauth2')
    access_token = social.extra_data['access_token']

    if request.method == 'POST':
        timeline = get_object_or_404(Timeline, pk=timeline_id)

        form = UserAddsMemoryForm(request.POST)

        if form.is_valid():
            c = Card()

            c.timeline_id = timeline
            if (form.cleaned_data.get('start_day') == 0):
                c.start_day = form.cleaned_data.get('start_day')
            if (form.cleaned_data.get('start_month') == 0):
                c.start_month = form.cleaned_data.get('start_month')
            c.start_year = form.cleaned_data.get('start_year')
            c.card_name = form.cleaned_data.get('card_name')
            c.description = form.cleaned_data.get('card_description')
            c.owner = request.user
            c.save()

            if (form.cleaned_data.get('file_id') != ''):
                m = Memory()
                m.card = c
                m.name = form.cleaned_data.get('file_name')
                m.description = form.cleaned_data.get('file_description')
                m.file_id = form.cleaned_data.get('file_id')
                m.file_type = form.cleaned_data.get('file_type')
                m.start_year = form.cleaned_data.get('start_year')
                m.save()


        return HttpResponseRedirect('/timeline/view/{}'.format(timeline_id))

    template_vars = {
        'form': form,
        'access_token': access_token,
        'parent_id': timeline.timeline_folder_id
    }

    return render(request, 'create_card.html', template_vars)


def edit_card(request, card_id):
    card = get_object_or_404(Card, pk=card_id)

    data = {
        'card_name': card.card_name,
        'start_day': card.start_day,
        'start_month': card.start_month,
        'start_year': card.start_year,
        'description': card.description
    }

    form = CardForm(initial=data)

    if request.method == 'POST':
        form = CardForm(request.POST)

        if form.has_changed():
            if form.is_valid():
                c = Card.objects.get(pk=card_id)
                c.start_day = form.cleaned_data.get('start_day')
                c.start_month = form.cleaned_data.get('start_month')
                c.start_year = form.cleaned_data.get('start_year')
                c.card_name = form.cleaned_data.get('card_name')
                c.description = form.cleaned_data.get('description')
                c.owner = request.user
                c.save()

                timeline = c.timeline_id

        return HttpResponseRedirect('/timeline/view/{}'.format(timeline.id))

    return render(request, 'edit_card.html', {'form': form})

class CardForm(ModelForm):
    class Meta:
        model = Card
        fields = ['start_day', 'start_month', 'start_year', 'card_name', 'description']
        widgets = {
            'card_name': forms.TextInput(attrs={'class':'form-control','placeholder':'Memory Name'}),
            'description': forms.Textarea(attrs={'class':'form-control','placeholder':'Description of the Memory.'}),
            'start_day': forms.Select(attrs={'class': 'form-control'}),
            'start_month': forms.Select(attrs={'class': 'form-control'}),
            'start_year': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'card_name': 'Memory Name',
            'start_day': 'Day',
            'start_month': 'Month',
            'start_year': 'Year'
        }

def add_memory(request, timeline_id, card_id):
    user = request.user

    timeline = get_object_or_404(Timeline, pk=timeline_id)

    social = user.social_auth.get(provider='google-oauth2')
    access_token = social.extra_data['access_token']

    template_vars = {
        'access_token': access_token,
        'parent_id': timeline.timeline_folder_id
    }

    return render(request, 'gpicker.html', template_vars)
