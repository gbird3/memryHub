from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Timeline(models.Model):
    '''A timeline of memories created by the user'''
    name = models.CharField(max_length=40)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    description = models.TextField(null=True, blank=True)
    image = models.CharField(null=True, blank=True, max_length=200)
