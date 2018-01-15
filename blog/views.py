# coding=utf-8

import logging

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from django.db import connection
from django.db.models import Count
import re
import sys

from blog.forms import RegForm, LoginForm

reload(sys)
sys.setdefaultencoding('utf-8')

logger = logging.getLogger('blog.views')

# Create your views here.


# 调用在setting里面配置的模板的变量
from blog.models import *


def global_setting(request):
	# 分类信息的获取（导航栏）
	category = Classification.objects.all()
	# 广告信息的获取（广告图片）
	ad = Ad.objects.filter().order_by('?')[:4]
	# 文章归档
	archive_list = Article.objects.date_distinct()
	# 浏览排行，评论排行，站长推荐，
	article_list_cc = Article.objects.filter().order_by('click_count')[:6]
	# 评论记数
	count_list_comment = Comment.objects.values('article').annotate(comment_count=Count('article')).order_by('-comment_count')
	article_list_comment = [Article.objects.get(pk=comment['article'])for comment in count_list_comment]
	article_list_recomment = Article.objects.filter().order_by('is_recomment')[:6]
	return {
		'category': category,
		'ad': ad,
		'archive_list': archive_list,
		'article_list_cc': article_list_cc,
		'article_list_comment': article_list_comment,
		'article_list_recomment': article_list_recomment,
		'SITE_NAME': settings.SITE_NAME,
		'SITE_DESC': settings.SITE_DESC,
	}


def index(request):
	try:
		# 分类信息的获取（导航栏）
		category = Classification.objects.all()
		# 广告信息的获取（广告图片）
		ad = Ad.objects.filter().order_by('?')[:4]
		# 最新文章列表
		article_list = Article.objects.all()
		# 分页
		article_list = getPage(request, article_list)

		# 	使用该方法原生的sql（不推荐）
		# print ('>>>>>>>>>')
		# cursor = connection.cursor()
		# cursor.execute("SELECT DISTINCT DATE_FORMAT(date_publsih, '%Y-%m') as col_date FROM blog.article ORDER BY date_publish")
		# row = cursor.fetchall()
		# print (row)
		# print ("<<<<<<<<<<<<<")

	except Exception as e:
		logger.error(e)

	# content = {
	# 	"ad": ad,
	# 	"category": category,
	# 	"article_list": article_list,
	# }
	return render(request, 'index.html', locals())


def to_article(request, article_id):
	try:
		article = Article.objects.filter(id=article_id)
		# 获取评论信息
		comments = Comment.objects.filter(article=article).order_by('id')
		comment_list =[]
		for comment in comments:
			for item in comment_list:
				if not hasattr(item, 'children_comment'):
					setattr(item, 'children_comment', [])
				if comment.pid == item:
					item.children_comment.append(comment)
					break
			if comment.pid is None:
				comment_list.append(comment)

	except Exception as e:
		logger.error(e)

	return render(request, 'article.html', locals())


# 归档
def archive(request):
	try:
		year = request.GET.get('year', None)
		month = request.GET.get('month', None)
		article_list = Article.objects.filter(date_publish__icontains=year+"-"+month)
		article_list = getPage(request,article_list)
	except Exception as e:
		logger.error(e)

	return render(request, 'archive.html', locals())


# 分页
def getPage(request, article_list):

	paginator = Paginator(article_list, 10)  # 分页列表 和每页列数
	try:
		page = int(request.GET.get('page', 1))  # 获取当前页
		article_list = paginator.page(page)  # 分页
	except(PageNotAnInteger, EmptyPage, InvalidPage):
		article_list = paginator.page(1)
	return article_list


# 提交评论
def comment_post(request):
	pass


# 退出登录
def do_logout(request):
	try:
		logout(request)
	except Exception as e:
		logger.error(e)
	return redirect(request.META['HTTP_REFERER'])


# 注册
def do_reg(request):
	try:
		if request.method == 'POST':
			reg_form = RegForm(request.POST)
			if reg_form.is_valid():
				# 注册
				user = User.objects.create(username=reg_form.cleaned_data['username'],
											email=reg_form.cleaned_data['email'],
											url=reg_form.cleaned_data['url'],
											password=make_password(reg_form.cleaned_data['password']),)
				user.save()

				# 登录
				user.backend = 'django.contrib.auth.backends.ModelBackend'  # 指定默认登录验证方式
				login(request, user)
				return redirect(request.POST.get('source_url'))
			else:
				return render(request, 'failure.html', {"reason": reg_form.errors})
		else:
			reg_form = RegForm()
	except Exception as e:
		logger.error(e)
	return render(request, 'reg.html', locals())


# 登录
def do_login(request):
	try:
		if request.method == 'POST':
			login_form = LoginForm(request.POST)
			if login_form.is_valid():
				# 登录
				username = login_form.cleaned_data['username']
				password = login_form.cleaned_data['password']
				user = authenticate(username=username, password=password)
				if user is not None:
					user.backend = 'django.contrib.auth.backends.ModelBackend'  # 指定默认登录验证方式
					login(request, user)
				else:
					return render(request, 'failure.html', {'reason': '登录验证失败'})
				return redirect(request.POST.get('source_url'))
			else:
				return render(request, 'failure.html', {'reason': login_form.errors})
		else:
			login_form = LoginForm()
	except Exception as e:
		logger.error(e)

	return render(request, 'login.html', locals())


# 分类
def category(request):
	pass