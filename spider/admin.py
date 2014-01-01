#coding = urt-8

from django.contrib import admin
from spider.models import *

class ArticleTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

class ArticleListAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'site', 'type', 'status')

    def get_ordering(self, request):
        return ["-id"]

class ArticleControlListAdmin(admin.ModelAdmin):
  list_display = ('id', 'article', 'control', 'arg1', 'arg2', 'arg3', 'arg4')

class ProductCompanyListAdmin(admin.ModelAdmin):
  list_display = ('id', 'name')

class CpuListAdmin(admin.ModelAdmin):
  list_display = ('id', 'fullname', 'name', 'cpu_cores', 'cpu_frequency', 'gpu', 'gpu_frequency', 'gpu_cores', 'sale_time', 'products', 'url')

  def get_ordering(self, request):
      return ['-products']

admin.site.register(SmtArticleType, ArticleTypeAdmin)
admin.site.register(SmtArticle, ArticleListAdmin)
admin.site.register(SmtArticleControl, ArticleControlListAdmin)
admin.site.register(SmtCompany, ProductCompanyListAdmin)
admin.site.register(SmtCpu, CpuListAdmin)
