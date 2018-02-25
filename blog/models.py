from django.db import models


# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=100, verbose_name="博主名字")
    gender = models.CharField(max_length=6, choices=(('male', u'男'), ('female', '女')), default='female',
                              verbose_name='性别')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')


class Blog(models.Model):
    title = models.CharField(max_length=100, verbose_name='标题')
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='博主名字')
    content = models.TextField(verbose_name='博客内容')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
