from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Timeline(models.Model):
    '''A timeline of memories created by the user'''
    owner_id = models.ForeignKey(User, on_delete=models.CASCADE)
    dateCreated = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    public = models.BooleanField(default=False)
    name = models.CharField(null=True, blank=True, max_length=40)
    description = models.TextField(null=True, blank=True)


class Person(models.Model):
    '''A Person for which a timeline exists. A Timeline can have many Persons and a Person can have many Timelines'''
