from django.shortcuts import render

# Create your views here.

def timelines(request):
    return render(request, 'timeline.html')


def create(request):
    return render(request, 'create.html')


def view(request):
    return render(request, 'view.html')
