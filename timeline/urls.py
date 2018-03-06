from django.urls import path

from . import views

urlpatterns = [
    path('', views.timelines, name='timelines'),
    path('view/<int:timeline_id>/', views.view, name='view'),
    path('edit/<int:timeline_id>/', views.edit_timeline, name='edit_timeline'),
    path('delete/<int:timeline_id>/', views.delete, name='delete'),
    path('memory/delete/<int:memory_id>/', views.delete_memory, name='delete_memory'),
    path('file/delete/<int:file_id>/', views.delete_file, name='delete_file'),
    path('file/edit/<int:file_id>/', views.edit_file, name='edit_file'),
    path('api/add-memory', views.api_add_memory, name='api_add_memory'),
    path('api/attach-file', views.api_attach_file, name='api_attach_file'),
    path('api/add-timeline', views.api_create_timeline, name='api_create_timeline'),
    path('api/share-timeline', views.api_share_timeline, name='api_share_timeline'),
    path('memory/attach/<int:memory_id>/', views.attach_files, name='attach_file'),
    path('sharing/<int:timeline_id>/', views.timeline_sharing, name='timeline_sharing'),
    path('test-email', views.testEmail, name="testEmail")
]
