# Generated by Django 2.0 on 2018-03-06 17:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('timeline', '0004_timeline_image_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='SharedTimeline',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('permission', models.CharField(default='read', max_length=10)),
                ('active', models.SmallIntegerField(default=1)),
                ('timeline', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timeline.Timeline')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
