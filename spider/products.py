# coding=utf-8

import os
import time
from django.db.models import *

from spider.models import *


class Product():
    cpu_list = []
    def __init__(self):
        self.cpu_list = []
        return

    def getCpuList(self):
        lst = SmtProductPad.objects.exclude(name="").filter(Q(saletime__contains="2013") | Q(saletime__contains="2012")).values("cpu").annotate(Count('cpu'))

        i = 0
        for item in lst:
            print item['cpu'],item['cpu__count']
            self.cpu_list.append(item['cpu'])
            if None == item or None == item['cpu']:
                continue

            cpu = SmtCpu()
            cpu.fullname = item['cpu']
            cpu.products = item['cpu__count']
            cpu.save_to_db()
            i = i + 1
            #if 20 == i:
            #    break

        #for cpu in self.cpu_list:
        #    lst = SmtProductPad.objects.exclude(name="").filter(cpu=cpu)
        #    for item in lst:
        #        print cpu,item.fullname,item.cpu_frequency,item.url

    def getProduct(self):
        lst = SmtCpu.objects.exclude(name="")
        for item in lst:
            lst_product = SmtProductPad.objects.filter(cpu__icontains=item.name).exclude(name="")
            for pitem in lst_product:
                #print pitem.fullname,pitem.name
                lst_article = SmtArticle.objects.filter(Q(title__icontains=pitem.name) | Q(content__icontains=pitem.name))
                for aitem in lst_article:
                    print aitem.title,item.name,pitem.name




        return
