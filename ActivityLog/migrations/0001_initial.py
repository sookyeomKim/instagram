# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-30 16:19
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity_type', models.CharField(max_length=50, verbose_name='ACTIVITY_TYPE')),
                ('img_url', models.CharField(max_length=255, verbose_name='IMG_URL')),
                ('account_id', models.CharField(max_length=50, verbose_name='ACCOUNT_ID')),
                ('tag_name', models.CharField(max_length=50, verbose_name='TAG_NAME')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='CREATE_DATE')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'activitylog',
                'verbose_name_plural': 'activitylogs',
                'db_table': 'ACTIVITYLOG',
            },
        ),
    ]
