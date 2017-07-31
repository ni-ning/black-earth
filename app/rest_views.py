#!/usr/bin/env python3
# -*-coding:utf-8 -*-
# __author__:Jonathan
# email:nining1314@gmail.com
from rest_framework import viewsets
from django.contrib.auth.models import User
from app import rest_serializers
from app import models


# ViewSets 定义了视图(view)的行为
class UserViewSet(viewsets.ModelViewSet):
    queryset = models.Account1.objects.all()
    serializer_class = rest_serializers.UserSerializer


class BranchViewSet(viewsets.ModelViewSet):
    queryset = models.Branch.objects.all()
    serializer_class = rest_serializers.BranchSerializer


class ContractViewSet(viewsets.ModelViewSet):
    queryset = models.Contract.objects.all()
    serializer_class = rest_serializers.ContractSerializer


class SourceViewSet(viewsets.ModelViewSet):
    queryset = models.Source.objects.all()
    serializer_class = rest_serializers.SourceSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = models.Course.objects.all()
    serializer_class = rest_serializers.CourseSerializer


class AccountViewSet(viewsets.ModelViewSet):
    queryset = models.Account.objects.all()
    serializer_class = rest_serializers.AccountSerializer


class ClassListViewSet(viewsets.ModelViewSet):
    queryset = models.ClassList.objects.all()
    serializer_class = rest_serializers.ClassListSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = models.Customer.objects.all()
    serializer_class = rest_serializers.CustomerSerializer
