#!/usr/bin/env python3
# -*-coding:utf-8 -*-
# __author__:Jonathan
# email:nining1314@gmail.com
from rest_framework import serializers
from django.contrib.auth.models import User
from app import models


# Serializers 定义了API的表现
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Account1
        fields = ('url', 'name', 'email', 'is_staff')


class BranchSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Branch
        fields = ('url', 'name',)


class ContractSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Contract
        fields = ('url', 'name', 'content')


class SourceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Source
        fields = ('url', 'name')


class CourseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Course
        fields = ('url', 'name')


class AccountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Account
        fields = ('url', 'username')


class ClassListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ClassList
        depth = 2
        fields = ('url', 'course', 'branch', 'semester', 'class_type', 'max_student_num', 'teachers', 'contract')


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Customer
        depth = 2
        fields = ('url', 'name', 'qq', 'weixin', 'phone', 'email',
                  'source', 'consult_courses', 'content', 'status',
                  'tags', 'consultant')


