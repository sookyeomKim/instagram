from django.db import models

# Create your models here.
from InstaInfo.models import InstaInfo


class HashTag(models.Model):
    tag_name = models.CharField('TAG_NAME', max_length=50, unique=True)
    insta_info = models.ManyToManyField(InstaInfo, through='HasgTagMembership')
    create_date = models.DateTimeField('CREATE_DATE', auto_now_add=True)
    modify_date = models.DateTimeField('MODIFY_DATE', auto_now=True)

    class Meta:
        db_table = 'HashTag'


class HasgTagMembership(models.Model):
    insta_info = models.ForeignKey(InstaInfo, on_delete=models.CASCADE)
    hash_tag = models.ForeignKey(HashTag, on_delete=models.CASCADE)
    create_date = models.DateTimeField('CREATE_DATE', auto_now_add=True)
    modify_date = models.DateTimeField('MODIFY_DATE', auto_now=True)
