# coding=utf-8
from __future__ import unicode_literals

from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


# 用户
class User(AbstractUser):
	avatar = models.ImageField(upload_to='./avatar/%Y/%m', default='avatar/default.png', max_length=200, verbose_name='头像')
	qq = models.CharField(max_length=20, blank=True, null=True,verbose_name='qq号码')
	mobile = models.CharField(max_length=11, blank=True, null=True, unique=True, verbose_name='手机号码')

	class Meta:
		verbose_name = '用户'
		verbose_name_plural = verbose_name
		ordering = ['-id']

	# 当print时，默认输出
	def __unicode__(self):
		return self.username


# tag(标签)
class Tag(models.Model):
	name = models.CharField(max_length=30, verbose_name='标签名称')

	class Meta:
		verbose_name = '标签'
		verbose_name_plural = verbose_name
		ordering = ['id']

	def __unicode__(self):
		return self.name


# 文章分类
class Classification(models.Model):
	name = models.CharField(max_length=30, verbose_name='分类名称')
	index = models.IntegerField(default=999, verbose_name='排序')

	class Meta:
		verbose_name = '文章分类'
		verbose_name_plural = verbose_name
		ordering = ['index', 'id']

	def __unicode__(self):
		return self.name


# 文章的管理类可以自己定义，添加新的查询方法
class ArticleManage(models.Manager):

	def date_distinct(self):
		distinct_date_list = []
		date_list = self.values('date_publish')
		for date in date_list:
			date = date['date_publish'].strftime(u'%Y/%m文章归档')
			if date not in distinct_date_list:
				distinct_date_list.append(date)
		return distinct_date_list


# 文章
class Article(models.Model):
	title = models.CharField(max_length=50, verbose_name='标题')
	desc = models.CharField(max_length=50, verbose_name='描述')
	content = models.TextField(verbose_name='内容')
	click_count = models.IntegerField(default=0, verbose_name='点赞次数')
	is_recomment = models.BooleanField(default=False, verbose_name='是否推荐')
	date_publish = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
	classification = models.ForeignKey(Classification, blank=True, null=True, verbose_name='分类')
	user = models.ForeignKey(User, verbose_name='用户')
	tag = models.ManyToManyField(Tag, verbose_name='标签')

	# 使用自定义的manage类，添加新的查询方法
	objects = ArticleManage()

	class Meta:
		verbose_name = '文章'
		verbose_name_plural = verbose_name
		ordering = ['-date_publish']

	def __unicode__(self):
		return self.title


# 评论
class Comment(models.Model):
	content = models.TextField(verbose_name='内容')
	date_publish = models.DateTimeField(auto_now_add=True, verbose_name='发表时间')
	user = models.ForeignKey(User, verbose_name='用户')
	article = models.ForeignKey(Article, blank=True, null=True, verbose_name='文章')
	pid = models.ForeignKey('self', blank=True, null=True, verbose_name='文章')  # 自己回复评论

	class Meta:
		verbose_name = '评论'
		verbose_name_plural = verbose_name
		ordering = ['date_publish']

	def __unicode__(self):
		return str(self.id)


# 广告
class Ad(models.Model):
	title = models.CharField(max_length=50, verbose_name='广告标题')
	decription = models.CharField(max_length=200, verbose_name='描述')
	image_url = models.ImageField(upload_to='./ad/%Y/%m', default='ad/default.png',  verbose_name='图片url')
	callback_url = models.CharField(max_length=200, verbose_name='回滚')
	date_publish = models.DateTimeField(auto_now_add=True, verbose_name='日期')
	index = models.IntegerField(default=999, verbose_name='排列顺序从小到大')

	class Meta:
		verbose_name = '广告'
		verbose_name_plural = verbose_name
		ordering = ['index','id']

	def __unicode__(self):
		return self.title


# 友情链接
class Links(models.Model):
	title = models.CharField(max_length=50, verbose_name='链接标题')
	decription = models.CharField(max_length=200, verbose_name='描述')
	callback_url = models.CharField(max_length=200,verbose_name='回滚')
	date_publish = models.DateTimeField(auto_now_add=True,verbose_name='日期')
	index = models.IntegerField(verbose_name='排列顺序')

	class Meta:
		verbose_name = '链接'
		verbose_name_plural = verbose_name
		ordering = ['index', 'id']

	def __unicode__(self):
		return self.title




