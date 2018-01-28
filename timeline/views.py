from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django import forms
from django.forms import ModelForm

from .models import Timeline, Card
# Create your views here.

@login_required(login_url='/login')
def timelines(request):

    timelines = Timeline.objects.filter(owner=request.user)

    return render(request, 'timeline.html', {'timelines': timelines})

@login_required(login_url='/login')
def create(request):
    form = CreateTimelineForm()

    if request.method == 'POST':
        form = CreateTimelineForm(request.POST)

        if form.is_valid():
            t = Timeline()
            t.owner = request.user
            t.name = form.cleaned_data.get('name')
            t.description = form.cleaned_data.get('description')

            t.save()

        return HttpResponseRedirect('/timeline/view')

    return render(request, 'create.html', {'form': form})


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

    cards = Card.objects.filter(timeline_id=timeline_id)

    template_vars = {
        'timeline': timeline,
        'cards': cards
    }

    return render(request, 'view.html', template_vars)


@login_required(login_url='/login')
def create_card(request, timeline_id):
    form = CardForm()
    if request.method == 'POST':
        timeline = get_object_or_404(Timeline, pk=timeline_id)

        form = CardForm(request.POST)

        if form.is_valid():
            c = Card()
            c.timeline_id = timeline
            c.start_day = form.cleaned_data.get('start_day')
            c.start_month = form.cleaned_data.get('start_month')
            c.start_year = form.cleaned_data.get('start_year')
            c.card_name = form.cleaned_data.get('card_name')
            c.description = form.cleaned_data.get('description')
            c.owner = request.user
            c.save()

            card_id = c.id
        return HttpResponseRedirect('/timeline/memory/{}/{}'.format(timeline_id, card_id))

    return render(request, 'create_card.html', {'form': form})


class CardForm(ModelForm):
    class Meta:
        model = Card
        fields = ['start_day', 'start_month', 'start_year', 'card_name', 'description']

def add_memory(request, timeline_id, card_id):
    print(timeline_id, card_id)

    return render(request, 'add_memory.html')
