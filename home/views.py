from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.contrib.auth import logout as auth_logout

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


def example1(request):
    user = request.user

    template_vars = {
        'user': user,
    }
    return render(request, 'example1.html',template_vars)


def exampleFile(request, file_id):
    user = request.user

    template_vars = {
        'user': user,
    }
    return render(request, 'example1.html',template_vars)


def edit_file(request, file_id):
    data = {
        'name': f.name,
        'description': f.description,
        'memory_id' : memory_id
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
        'form': form,
        'file': f,
        'memory_id' : memory_id
    }

    return render(request, 'edit_file.html', template_vars)
