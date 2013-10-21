# coding=utf-8

from django.db import models
import datetime

#aritcle type
class SmtArticleType(models.Model):
    name = models.CharField(max_length=32)
    iname = models.CharField(max_length=32) 
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
    status = models.BooleanField(default=True)
    
    def __unicode__(self):
        return self.title

#aritcle control
class SmtArticleControl(models.Model):
  article = models.ForeignKey(SmtArticle)
  control = models.IntegerField()
  arg1 = models.IntegerField(default=0)
  arg2 = models.BooleanField(default=True)
  arg3 = models.CharField(max_length=255, null=True)
  arg4 = models.CharField(max_length=255, null=True)

  def __unicode__(self):
    return str(self.article.id) + self.article.title

#img resource
class SmtImgResource(models.Model):
  original = models.CharField(max_length=255)
  real = models.CharField(max_length=255)


