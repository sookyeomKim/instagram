# Generated by Django 2.0.1 on 2018-03-31 16:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ActivityLog', '0002_auto_20170901_0204'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activitylog',
            name='tag_name',
        ),
    ]
