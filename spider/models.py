# coding=utf-8

from django.db import models
import datetime

#aritcle type
class SmtArticleType(models.Model):
    name = models.CharField(max_length=32)
    
    def __unicode__(self):
        return self.name

#article
class SmtArticle(models.Model):
    title = models.CharField(max_length=128)
    url = models.CharField(max_length=128)
    content = models.TextField(null=True)
    site = models.CharField(max_length=64)
    pubtime = models.DateTimeField(default=datetime.datetime.now())
    updatetime = models.DateTimeField(auto_now=True, default=datetime.datetime.now())
    type = models.ForeignKey(SmtArticleType, null=True)
    description = models.CharField(max_length=128, null=True)
    pic = models.CharField(max_length=512, null=True)
    
    def __unicode__(self):
        return self.title

