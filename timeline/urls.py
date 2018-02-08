from django.urls import path

from . import views

urlpatterns = [
    path('', views.timelines, name='timelines'),
    path('create', views.create, name='create'),
    path('view/<int:timeline_id>/', views.view, name='view'),
    path('edit/<int:timeline_id>/', views.edit, name='edit'),
    path('add-memory/<int:timeline_id>/', views.add_memory, name='add_memory'),
    # path('memory/<int:timeline_id>/<int:card_id>/', views.add_memory, name='add_memory'),
    path('memory/edit/<int:memory_id>/', views.edit_memory, name='edit_memory'),
    # path('fileupload/', views.google_picker, name='google_picker'),
]
