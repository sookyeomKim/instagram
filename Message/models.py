from django.db import models

# Create your models here.
from InstaInfo.models import InstaInfo


class Message(models.Model):
    message_content = models.CharField('MESSAGE_CONTENT', max_length=255, unique=True)
    insta_info = models.ManyToManyField(InstaInfo, through='MessageMembership')
    create_date = models.DateTimeField('CREATE_DATE', auto_now_add=True)
    modify_date = models.DateTimeField('MODIFY_DATE', auto_now=True)

    class Meta:
        db_table = 'Message'


class MessageMembership(models.Model):
    insta_info = models.ForeignKey(InstaInfo, on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
