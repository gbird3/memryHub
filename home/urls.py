from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('logout', views.logout, name='logout'),
    path('login', views.login, name='login'),
    path('example1', views.example1, name='example1'),
    path('example_file_1', views.example_file_1, name="example_file_1"),
    path('example_file_2', views.example_file_2, name="example_file_2"),
    path('example_file_3', views.example_file_3, name="example_file_3"),
    path('example_file_4', views.example_file_4, name="example_file_4"),
    path('example_file_5', views.example_file_5, name="example_file_5"),
    path('groups', views.groups, name='groups'),
    path('groups/<int:group_id>/users', views.group_users, name='group_users'),
    path('privacy', views.privacy, name='privacy'),
    path('auth_error', views.auth_error, name='auth_error')
]
