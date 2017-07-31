#!/usr/bin/env python3
# -*-coding:utf-8 -*-
# __author__:Jonathan
# email:nining1314@gmail.com

from django.conf import settings

for app_name in settings.INSTALLED_APPS:
    try:
        __import__("%s.%s" % (app_name, 'luffy_admin'))
    except ImportError:
        pass
