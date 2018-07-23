from django.db import models

# Create your models here.
from InstaInfo.models import InstaInfo


class Prevent(models.Model):
    tag_name = models.CharField('TAG_NAME', max_length=50, unique=True)
    insta_info = models.ManyToManyField(InstaInfo, through='PreventMembership')
    create_date = models.DateTimeField('CREATE_DATE', auto_now_add=True)
    modify_date = models.DateTimeField('MODIFY_DATE', auto_now=True)

    class Meta:
        db_table = 'Prevent'


class PreventMembership(models.Model):
    insta_info = models.ForeignKey(InstaInfo, on_delete=models.CASCADE)
    prevent_tag = models.ForeignKey(Prevent, on_delete=models.CASCADE)
