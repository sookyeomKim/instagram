from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class InstaInfo(models.Model):
    insta_account = models.CharField('INSTA_ACCOUNT', max_length=50, unique=True)
    insta_passwd = models.CharField('INSTA_PASSWD', max_length=50)
    onoff_trigger = models.BooleanField('ONOFF_TRIGGER', default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    create_date = models.DateTimeField('CREATE_DATE', auto_now_add=True)
    modify_date = models.DateTimeField('MODIFY_DATE', auto_now=True)

    class Meta:
        db_table = 'InstaInfo'
