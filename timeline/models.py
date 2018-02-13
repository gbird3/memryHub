from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Timeline(models.Model):
    '''A timeline of memories created by the user'''
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True, max_length=500)
    image = models.CharField(null=True, blank=True, max_length=200)
    timeline_folder_id = models.CharField(null=True, blank=True, max_length=300)
    date_created = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    active = models.SmallIntegerField(default=1)


class Memory(models.Model):
    '''A specific aspect of the timeline that can hold memories'''
    name = models.CharField(max_length=100)
    timeline_id = models.ForeignKey(Timeline, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True, max_length=500)
    folder_id = models.CharField(null=True, blank=True, max_length=300)
    day = models.PositiveSmallIntegerField(null=True, blank=True, db_index=True)
    month = models.PositiveSmallIntegerField(null=True, blank=True, db_index=True)
    year = models.PositiveSmallIntegerField(db_index=True)
    city = models.CharField(null=True, blank=True, max_length=100)
    state = models.CharField(null=True, blank=True, max_length=100)
    country = models.CharField(null=True, blank=True, max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    active = models.SmallIntegerField(default=1)

class File(models.Model):
    '''Files attached to a memory (Pictures, Videos, Audio, Text).'''
    memory = models.ForeignKey(Memory, on_delete=models.CASCADE)
    name = models.CharField(null=True, max_length=200)
    file_type = models.CharField(null=True, blank=True, max_length=50)
    file_id = models.CharField(null=True, blank=True, max_length=300)
    description = models.TextField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    active = models.SmallIntegerField(default=1)
