# -*- coding:utf-8 -*-


from django.conf.urls import url
from blog.views import *


urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'article/(?P<article_id>\d+)/$', to_article, name='to_article'),
    url(r'^add_comment/(?P<article_title>\d+)/$', to_article, name='to_article'),
    url(r'^comment/post/$', comment_post, name="comment_post"),
    url(r'^logout$', do_logout, name="logout"),
    url(r'^reg', do_reg, name="reg"),
    url(r'login', do_login, name="login"),
    url(r'^category/$', category, name="category"),
    url(r'^archive/$', archive, name='archive'),
]







