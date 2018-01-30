from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserInfo(models.Model):
    '''Stores the information on the user's root google folder where we will store their files'''
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    root_folder_id = models.CharField(null=True, blank=True, max_length=300)
