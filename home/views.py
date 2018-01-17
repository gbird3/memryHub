from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.contrib.auth import logout as auth_logout

def index(request):
    return render(request, 'index.html')

# Create your views here.



def logout(request):
    """Logs out a user"""
    auth_logout(request)
    return render_to_response('index.html')
