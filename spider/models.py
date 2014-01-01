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

#company
class SmtCompany(models.Model):
  name = models.CharField(max_length=64)

  def __unicode__(self):
    return self.name

#cpu
class SmtCpu(models.Model):
  fullname = models.CharField(max_length=64)
  name = models.CharField(max_length=32, default="", null=True)
  company = models.CharField(max_length=64, default="0", null=True)
  craft = models.CharField(max_length=32, default="0", null=True)
  cpu_cores = models.CharField(max_length=32,default="0", null=True)
  cpu_frequency = models.CharField(max_length=32, default="0", null=True)
  gpu = models.CharField(max_length=32, default="0", null=True)
  gpu_cores = models.CharField(max_length=32, default="0", null=True)
  gpu_frequency = models.CharField(max_length=32, default="0", null=True)
  sale_time = models.CharField(max_length=64, default="0", null=True)
  url = models.CharField(max_length=255, default="", null=True)
  products = models.IntegerField(default=0)

  def __unicode__(self):
      return self.name

  def save_to_db(self):
      cpu = SmtCpu.objects.filter(fullname=self.fullname)
      if None != cpu and 0 < len(cpu):
          cpu = cpu[0]
          cpu.products = self.products
          cpu.save()
          print "update cpu"
      else:
          self.save()
          print "save cpu"
      return


#product
class SmtProductPad(models.Model):
  url = models.CharField(max_length=128)
  fullname = models.CharField(max_length=128)
  name = models.CharField(max_length=64)
  lock_name = models.BooleanField(default=False)
  company = models.ForeignKey(SmtCompany)
  lock_company = models.BooleanField(default=False)
  nametype = models.CharField(max_length=64, null=True)
  lock_nametype = models.BooleanField(default=False)
  saletime = models.CharField(max_length=64, null=True)
  lock_saletime = models.BooleanField(default=False)
  system = models.CharField(max_length=64, null=True)
  lock_system = models.BooleanField(default=False)
  system_version = models.CharField(max_length=32, null=True)
  lock_system_version = models.BooleanField(default=False)
  cpu = models.CharField(max_length=64, null=True)
  lock_cpu = models.BooleanField(default=False)
  cpu_frequency = models.CharField(max_length=32, null=True)
  lock_cpu_frequency = models.BooleanField(default=False)
  cpucores = models.CharField(max_length=32,null=True)
  lock_cpucores = models.BooleanField(default=False)
  gpu = models.CharField(max_length=32, null=True)
  lock_gpu = models.BooleanField(default=False)
  gpucores = models.CharField(max_length=32, null=True)
  lock_gpucores = models.BooleanField(default=False)
  memory = models.CharField(max_length=32, null=True)
  lock_memory = models.BooleanField(default=False)
  storage = models.CharField(max_length=32, null=True)
  lock_storage = models.BooleanField(default=False)
  storage_ext = models.CharField(max_length=32, null=True)
  lock_storage_ext = models.BooleanField(default=False)
  screen_size = models.CharField(max_length=32, null=True)
  lock_screen_size = models.BooleanField(default=False)
  screen_resolution = models.CharField(max_length=32, null=True)
  lock_screen_resolution = models.BooleanField(default=False)
  screen_ppi = models.CharField(max_length=32, null=True)
  lock_screen_ppi = models.BooleanField(default=False)
  screen_character = models.CharField(max_length=32, null=True)
  lock_screen_character = models.BooleanField(default=False)
  camera = models.CharField(max_length=32, null=True)
  lock_camera = models.BooleanField(default=False)
  battery_life = models.CharField(max_length=32, null=True)
  lock_battery_life = models.BooleanField(default=False)
  size = models.CharField(max_length=32, null=True)
  lock_size = models.BooleanField(default=False)
  weight = models.CharField(max_length=32, null=True)
  lock_weight = models.BooleanField(default=False)

  def save_to_db(self):
    find = SmtProductPad.objects.filter(fullname=self.fullname)
    if None != find and len(find) > 0:
        node = find[0]
        self.id = node.id
        if True == node.lock_name:
            self.name = node.name
        if True == node.lock_company:
            self.company = node.company
        if True == node.lock_nametype:
            self.nametype = node.nametype
        if True == node.lock_saletime:
            self.saletime = node.saletime
        if True == node.lock_system:
            self.system = node.system
        if True == node.lock_system_version:
            self.system_version = node.system_version
        if True == node.lock_cpu:
            self.cpu = node.cpu
        if True == node.lock_cpu_frequency:
            self.cpu_frequency = node.cpu_frequency
        if True == node.lock_gpu:
            self.gpu = node.gpu
        if True == node.lock_gpucores:
            self.gpucores = node.gpucores
        if True == node.lock_memory:
            self.memory = node.memory
        if True == node.lock_storage:
            self.storage = node.storage
        if True == node.lock_storage_ext:
            self.storage_ext = node.storage_ext
        if True == node.lock_screen_size:
            self.screen_size = node.screen_size
        if True == node.lock_screen_resolution:
            self.screen_resolution = node.screen_resolution
        if True == node.lock_screen_ppi:
            self.screen_ppi = node.screen_ppi
        if True == node.lock_camera:
            self.camera = node.camera
        if True == node.lock_battery_life:
            self.battery_life = node.battery_life
        if True == node.lock_size:
            self.size = node.size
        if True == node.lock_weight:
            self.weight = node.weight
    
    try:
        self.save()
        print '------',self.fullname, 'save ok------'
    except:
        print '------ERROR:',self.fullname,'save fail------'

  def __unicode__(self):
    return self.name
