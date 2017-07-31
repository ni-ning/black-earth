#!/usr/bin/env python3
# -*-coding:utf-8 -*-
# __author__:Jonathan
# email:nining1314@gmail.com

"""
name = 'Linda'
print("My namme is %s" % name)
print("My name is {name}".format(name=name))

from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

# 用来创建用户
class MyUserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        user = self.create_user(
            email,
            password=password,
            name=name,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


# 定制账号基本信息
class Account(AbstractBaseUser):

    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=32)
    role = models.ForeignKey("Role", blank=True, null=True)
    customer = models.OneToOneField("Customer", blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    # 其他基本信息......
"""


def index(x):
    def get():
        print(x)
    return get

f = index(1)
print(f.__closure__[0].cell_contents)
f()

