from django.urls import path

from . import views

urlpatterns = [
    path('', views.timelines, name='timelines'),
    path('create', views.create, name='create'),
    path('view/<int:timeline_id>/', views.view, name='view'),
    path('edit/<int:timeline_id>/', views.edit, name='edit'),
    path('delete/<int:timeline_id>/', views.delete, name='delete'),
    path('memory/delete/<int:memory_id>/', views.delete_memory, name='delete_memory'),
    path('file/delete/<int:file_id>/', views.delete_file, name='delete_file'),
    path('api/add-memory', views.api_add_memory, name='api_add_memory'),
    path('api/attach-file', views.api_attach_file, name='api_attach_file'),
    path('memory/attach/<int:memory_id>/', views.attach_files, name='attach_file'),
]
