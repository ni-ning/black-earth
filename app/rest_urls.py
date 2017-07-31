#!/usr/bin/env python3
# -*-coding:utf-8 -*-
# __author__:Jonathan
# email:nining1314@gmail.com

from django.conf.urls import url, include
from app import rest_views
from rest_framework import routers

from app import views

# /api/users   -->  UserViewSet
router = routers.DefaultRouter()
router.register(r'users', rest_views.UserViewSet)
router.register(r'branches', rest_views.BranchViewSet)
router.register(r'contracts', rest_views.ContractViewSet)
router.register(r'sources', rest_views.SourceViewSet)
router.register(r'courses', rest_views.CourseViewSet)
router.register(r'class-lists', rest_views.ClassListViewSet)
router.register(r'customers', rest_views.CustomerViewSet)
router.register(r'accounts', rest_views.AccountViewSet)


# 将rest_framework路由与Django路由关联起来
# 登录可视化API的URLs
urlpatterns = [
    url(r'^v1/', include(router.urls)),
    url(r'^branch-list/$', views.branch_list),
    url(r'^branch-detail-(\d+)/$', views.branch_detail),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
