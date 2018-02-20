from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django import forms
from django.forms import ModelForm

import json

from ..models import Timeline, Memory, File
from ..gdrive import createFolder, changeFileData

class EditFileForm(forms.Form):
    name = forms.CharField(label='File Name', required=True, max_length=100, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'File Name'}))
    description = forms.CharField(label='File Description', required=False, max_length=100, widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Short description of your file.'}))

@login_required(login_url='/login')
def edit_file(request, file_id):
    f = File.objects.get(pk=file_id)

    data = {
        'name': f.name,
        'description': f.description
    }

    form = EditFileForm(initial=data)

    if request.method == 'POST':
        form = EditFileForm(request.POST)
        if form.has_changed():
            if form.is_valid():
                f = File.objects.get(pk=file_id)

                response = changeFileData(request.user, f.file_id, form.cleaned_data.get('name'), form.cleaned_data.get('description'))

                f.name = form.cleaned_data.get('name')
                f.description = form.cleaned_data.get('description')
                f.save()

        return HttpResponseRedirect('/timeline/memory/attach/{}'.format(f.memory.id))


    template_vars = {
        'form': form
    }

    return render(request, 'edit_file.html', template_vars)





@login_required(login_url='/login')
def delete_file(request, file_id):
    f = File.objects.get(pk=file_id)
    f.active = 0
    f.save()

    memory = f.memory

    return HttpResponseRedirect('/timeline/memory/attach/{}'.format(memory.id))
