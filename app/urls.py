#!/usr/bin/env python3
# -*-coding:utf-8 -*-
# __author__:Jonathan
# email:nining1314@gmail.com
from django.conf.urls import url
from app import views

urlpatterns = [
    url(r'^app/customer_list/$', views.customer_list),
    url(r'^(\w+)/(\w+)/(\d+)/change/$', views.customer_obj_change, name="table_obj_change"),
    url(r'^(\w+)/(\w+)/add/$', views.customer_obj_add, name="table_obj_add"),
    url(r'^(\w+)/(\w+)/(\d+)/delete/$', views.customer_object_del, name="object_del"),

    url(r'^app/customer_followup_list/$', views.customer_followup_list),
]