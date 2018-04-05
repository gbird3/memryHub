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
    return render(request, 'example1.html')


def example_file_1(request):
    return render(request, 'example_file_1.html')

def example_file_2(request):
    return render(request, 'example_file_2.html')

def example_file_3(request):
    return render(request, 'example_file_3.html')

def example_file_4(request):
    return render(request, 'example_file_4.html')

def example_file_5(request):
    return render(request, 'example_file_5.html')
