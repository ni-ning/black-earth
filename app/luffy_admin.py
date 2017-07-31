#!/usr/bin/env python3
# -*-coding:utf-8 -*-
# __author__:Jonathan
# email:nining1314@gmail.com

print('---------app/luffy_admin.py-----------')
from app import models
from luffyAdmin.admin_base import site, BaseAdmin


class CustomerAdmin(BaseAdmin):
    list_display = ['id', 'name', 'qq', 'consultant', 'source', 'status']
    list_filter = ['consultant', 'source', 'status']
    list_per_page = 5
    search_fields = ['name', 'qq', 'source__name']
    filter_horizontal = ['tags', 'consult_courses']


class CourseAdmin(BaseAdmin):
    list_display = ['name', 'period', 'price']
    search_fields = ['name', ]

site.register(models.Customer, CustomerAdmin)
site.register(models.ClassList)
site.register(models.Course, CourseAdmin)
