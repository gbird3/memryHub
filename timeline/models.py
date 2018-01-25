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

# DAY_CHOICES = (
#     ('1', 1),
#     ('2', 2),
#     ('3', 3),
#     ('4', 4),
#     ('5', 5),
#     ('6', 6),
#     ('7', 7),
#     ('8', 8),
#     ('9', 9),
#     ( '10', 10),
#     ( '11', 11),
#     ( '12', 12),
#     ( '13', 13),
#     ( '14', 14),
#     ( '15', 15),
#     ( '16', 16),
#     ( '17', 17),
#     ( '18', 18),
#     ( '19', 19),
#     ( '20', 20),
#     ( '21', 21),
#     ( '22', 22),
#     ( '23', 23),
#     ( '24', 24),
#     ( '25', 25),
#     ( '26', 26),
#     ( '27', 27),
#     ( '28', 28),
#     ( '29', 29),
#     ( '30', 30),
#     ( '31', 31),
# )

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
    end_year = models.PositiveSmallIntegerField(choices=YEAR_CHOICES)

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
