#!/usr/bin/env python3
# -*-coding:utf-8 -*-
# __author__:Jonathan
# email:nining1314@gmail.com

print('-----teacher/luffy_admin.py----------')
from teacher import models
from luffyAdmin.admin_base import site, BaseAdmin

site.register(models.TeacherInfo)
