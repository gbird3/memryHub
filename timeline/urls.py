from django.urls import path

from . import views

urlpatterns = [
    path('', views.timelines, name='timelines'),
    path('create', views.create, name='create'),
    path('view', views.view, name='view'),
]
