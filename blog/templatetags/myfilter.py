# -*- coding:utf-8 -*-

from django import template
register = template.Library()


# 定义一个数字月份转为大写数字月份 如：8 为八
@register.filter
def mouth_to_upper(key):
	return ["一", "二", "三", "四", "五", "六", "七", "八", "九", "十", "十一", "十二"][key.month-1]


# 注册过滤器
# register.filter('mouth_to_upper', mouth_to_upper)

