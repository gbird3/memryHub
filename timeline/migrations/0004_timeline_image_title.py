# Generated by Django 2.0 on 2018-02-24 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timeline', '0003_auto_20180224_1756'),
    ]

    operations = [
        migrations.AddField(
            model_name='timeline',
            name='image_title',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
