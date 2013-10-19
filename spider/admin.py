#coding = urt-8

from django.contrib import admin
from spider.models import *

class ArticleTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

class ArticleListAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'site', 'type')

admin.site.register(SmtArticleType, ArticleTypeAdmin)
admin.site.register(SmtArticle, ArticleListAdmin)
