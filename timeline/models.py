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
    timeline_folder_id = models.CharField(null=True, blank=True, max_length=300)

DAY_CHOICES = ( tuple((i, str(i)) for i in range(1, 31)) )

MONTH_CHOICES = (
    (1, 'January'),
    (2, 'Febuary'),
    (3, 'March'),
    (4, 'April'),
    (5, 'May'),
    (6, 'June'),
    (7, 'July'),
    (8, 'August'),
    (9, 'September'),
    (10, 'October'),
    (11, 'November'),
    (12, 'December'),
)

YEAR_CHOICES = ( tuple((i, str(i)) for i in range(1900, 2018)) )

class AbstractDate(models.Model):
    '''Abstract instance of date to make adding start and end day, month, and year to Card and Memory'''
    start_day = models.PositiveSmallIntegerField(null=True, blank=True, choices=DAY_CHOICES)
    start_month = models.PositiveSmallIntegerField(null=True, blank=True, choices=MONTH_CHOICES)
    start_year = models.PositiveSmallIntegerField(choices=YEAR_CHOICES)
    end_day = models.PositiveSmallIntegerField(null=True, blank=True, choices=DAY_CHOICES)
    end_month = models.PositiveSmallIntegerField(null=True, blank=True, choices=MONTH_CHOICES)
    end_year = models.PositiveSmallIntegerField(null=True, blank=True, choices=YEAR_CHOICES)

    class Meta:
        abstract = True

class Card(AbstractDate):
    '''A specific aspect of the timeline that can hold memories'''
    card_name = models.CharField(max_length=40)
    timeline_id = models.ForeignKey(Timeline, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)


file_choices = (
    (0, 'Written Memory'),
    (1, 'Audio'),
    (2, 'Video'),
    (3, 'Picture'),
)

class Memory(AbstractDate):
    '''A specific instance of a Memory.'''
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    file_type = models.CharField(null=True, blank=True, choices=file_choices, max_length=30)
    description = models.TextField(null=True, blank=True)
    file_id = models.CharField(null=True, blank=True, max_length=300)
    city = models.CharField(null=True, blank=True, max_length=100)
    state = models.CharField(null=True, blank=True, max_length=100)
    country = models.CharField(null=True, blank=True, max_length=100)
