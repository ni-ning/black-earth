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
    actions = ['enroll']
    readonly_fields = ['name', 'qq', 'tags', 'consultant']

    def enroll(self, request, querysets):
        print("--enroll--", request, querysets)
        querysets.update(status=0)

    enroll.short_description = '批量报名'


class CourseAdmin(BaseAdmin):
    list_display = ['name', 'period', 'price']
    search_fields = ['name', ]


class RoleAdmin(BaseAdmin):
    list_display = ['name', 'menus']
    filter_horizontal = ['menus']

site.register(models.Customer, CustomerAdmin)
site.register(models.ClassList)
site.register(models.Course, CourseAdmin)
site.register(models.Role, RoleAdmin)
site.register(models.Menu)
site.register(models.SubMenu)