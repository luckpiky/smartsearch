#coding = urt-8

from django.contrib import admin
from spider.models import *

class ArticleTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

class ArticleListAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'site', 'type', 'status')

class ArticleControlListAdmin(admin.ModelAdmin):
  list_display = ('id', 'article', 'control', 'arg1', 'arg2', 'arg3', 'arg4')

admin.site.register(SmtArticleType, ArticleTypeAdmin)
admin.site.register(SmtArticle, ArticleListAdmin)
admin.site.register(SmtArticleControl, ArticleControlListAdmin)
