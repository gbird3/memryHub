from django.urls import path

from . import views

urlpatterns = [
    path('', views.timelines, name='timelines'),
    path('create', views.create, name='create'),
    path('view/<int:timeline_id>/', views.view, name='view'),
    path('edit/<int:timeline_id>/', views.edit, name='edit'),
    path('create-card/<int:timeline_id>/', views.create_card, name='create_card'),
    path('memory/<int:timeline_id>/<int:card_id>/', views.add_memory, name='add_memory'),
    path('card/edit/<int:card_id>/', views.edit_card, name='edit_card'),
    path('fileupload/', views.google_picker, name='google_picker'),
]
