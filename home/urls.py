from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('logout', views.logout, name='logout'),
    path('login', views.login, name='login'),
    path('groups', views.groups, name='groups')
]
