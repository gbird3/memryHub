# Generated by Django 2.0 on 2018-01-30 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timeline', '0003_auto_20180127_2002'),
    ]

    operations = [
        migrations.AddField(
            model_name='timeline',
            name='timeline_folder_id',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
