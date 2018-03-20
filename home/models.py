from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserInfo(models.Model):
    '''Stores the information on the user's root google folder where we will store their files'''
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    root_folder_id = models.CharField(null=True, blank=True, max_length=300)

class Group(models.Model):
    '''A group for users'''
    name = models.CharField(null=True, max_length=200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    active = models.SmallIntegerField(default=1)

class UserHasGroup(models.Model):
    '''Users that belong to a group'''
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)