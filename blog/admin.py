# -*- coding: utf-8 -*-
from django.contrib import admin
from blog.models import *

# Register your models here.


# 文章的管理类
class ArticleAdmin(admin.ModelAdmin):
	# 编辑表单的显示
	fieldsets = (
		(None, {
			'fields': ('title', 'user', 'desc', 'content')
		}),
		('Advanced options', {
			'classes': ('collapse',),
			'fields': ('click_count', 'is_recomment', 'classification', 'tag')
		}),
	)
	# 添加之后的列表显示
	list_display = ('title', 'user', 'desc', 'classification')
	search_fields = ['title', 'user', 'classification']
	ordering = ['date_publish']
	list_filter = ['user', 'title']

	class Media:
		js = (
			'/static/js/kindeditor-4.1.10/kindeditor-min.js',
			'/static/js/kindeditor-4.1.10/lang/zh_CN.js',
			'/static/js/kindeditor-4.1.10/config.js',
		)


# 用户的管理类
class UserAdmin(admin.ModelAdmin):
	exclude = ('first_name', 'last_name')
	list_display = ('username', 'password', 'is_superuser', 'qq', 'mobile', 'email', 'date_joined')
	list_filter = ['username']
	ordering = ['-date_joined']


# 评论的管理类
class CommentAdmin(admin.ModelAdmin):
	list_display = ['article', 'user', 'content', 'date_publish', 'pid']
	list_filter = ['user']

	class Media:
		js = (
			'/static/js/kindeditor-4.1.10/kindeditor-min.js',
			'/static/js/kindeditor-4.1.10/lang/zh_CN.js',
			'/static/js/kindeditor-4.1.10/config.js',
		)


# 文章分类
class ClassificationAdmin(admin.ModelAdmin):
	list_display = ['name', 'index', ]
	list_filter = ['name']


# 广告的管理类
class AdAdmin(admin.ModelAdmin):
	list_display = ['title', 'decription', 'image_url', 'callback_url', 'date_publish', 'index', ]


# 友情链接的管理类
class LinksAdmin(admin.ModelAdmin):
	list_display = ['title', 'decription', 'callback_url', 'date_publish', 'index', ]


admin.site.register(User, UserAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Tag)
admin.site.register(Classification,ClassificationAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Ad, AdAdmin)
admin.site.register(Links, LinksAdmin)

