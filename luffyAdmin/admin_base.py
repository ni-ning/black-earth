#!/usr/bin/env python3
# -*-coding:utf-8 -*-
# __author__:Jonathan
# email:nining1314@gmail.com


class BaseAdmin(object):
    list_display = ()
    list_filter = ()
    list_per_page = 10
    search_fields = []
    filter_horizontal = []


class AdminSite(object):
    def __init__(self):
        self.registered_admins = {}
        """最终形态如下所示，其中'customer': admin_class --> admin_class.model
        self.registered_admins = {
            'app':{
                'customer': <class 'app.luffy_admin.CustomerAdmin'>,   # 有admin_class
                'classlist': <class 'luffyAdmin.admin_base.BaseAdmin'> # 无admin_class
                ...
                }
            'teacher':{
                'teachertest': <class 'luffyAdmin.admin_base.BaseAdmin'>
                ...
                }
            ...
            }
        """

    def register(self, model_or_iterable, admin_class=None, **options):
        """
        1. 负责把每个app下的表注册self.registered_admins集合里
        2. 参数 model_or_iterable: 表类，如models.Customer
        3, 参数 admin_class: 定制的展示类，如CustomerAdmin
        4. 已知条件 --推导出---> 未知条件，达到解决问题的目的
        """
        # if not admin_class:
        #     admin_class = BaseAdmin

        if not admin_class:
            admin_class = BaseAdmin()

        admin_class.model = model_or_iterable          # 把库类装到admin_class中，以供simple_tags调用
        app_label = model_or_iterable._meta.app_label  # 得到应用程序名 如app，teacher

        if app_label not in self.registered_admins:
            self.registered_admins[app_label] = {}
        self.registered_admins[app_label][model_or_iterable._meta.model_name] = admin_class

        # model_or_iterable._meta.app_label , 应用程序名，如app
        # model_or_iterable._meta.model_name，库表名，如customer


site = AdminSite()

