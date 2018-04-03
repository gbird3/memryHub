from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('logout', views.logout, name='logout'),
    path('login', views.login, name='login'),
    path('groups', views.groups, name='groups'),
    path('groups/<int:group_id>/users', views.group_users, name='group_users')
]
