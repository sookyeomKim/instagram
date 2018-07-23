from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from InstaInfo.models import InstaInfo


class ActivityLog(models.Model):
    activity_type = models.CharField('ACTIVITY_TYPE', max_length=50)
    #img_url = models.CharField('IMG_URL', max_length=255)
    account_id = models.CharField('ACCOUNT_ID', max_length=50)
    insta_info = models.ForeignKey(InstaInfo, null=True, on_delete=models.CASCADE)
    create_date = models.DateTimeField('CREATE_DATE', auto_now_add=True)

    class Meta:
        db_table = 'ActivityLog'
        ordering = ('-create_date',)
