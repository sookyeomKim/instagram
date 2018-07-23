from django.db import models

# Create your models here.
from InstaInfo.models import InstaInfo


class CountLog(models.Model):
    follow_count = models.CharField('FOLLOW_COUNT', max_length=50)
    follower_count = models.CharField('FOLLOWER_COUNT', max_length=50)
    insta_info = models.ForeignKey(InstaInfo, null=True, on_delete=models.CASCADE)
    create_date = models.DateTimeField('CREATE_DATE', auto_now_add=True)

    class Meta:
        db_table = 'CountLog'
        ordering = ('-create_date',)

