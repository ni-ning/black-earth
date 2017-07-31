#!/usr/bin/env python3
# -*-coding:utf-8 -*-
# __author__:Jonathan
# email:nining1314@gmail.com
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from app import models
from django.db.models import Q


@login_required
def dashboard(request):
    return render(request, 'index.html')


@login_required
def index(request):
    return render(request, 'base.html')


def account_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect(request.GET.get('next') or '/')
    return render(request, 'login.html')


def account_logout(request):
    logout(request)
    return redirect('/')


def test(reqeust):
    # 测试 Q 用法
    query = '大'
    search_fields = ['name', 'qq']
    q1 = Q()
    q1.connector = "OR"
    for field in search_fields:
        para = "%s__icontains" % field
        q1.children.append((para, query))
    querysets = models.Customer.objects.filter(q1, name='小强')
    print(querysets)
    return HttpResponse('OK')