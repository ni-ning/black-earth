#!/usr/bin/env python3
# -*-coding:utf-8 -*-
# __author__:Jonathan
# email:nining1314@gmail.com
from django.forms import ModelForm

"""

from app import models
class CustomerForm(ModelForm):
    class Meta:
        model = models.Customer
        fields = '__all__'

class CourseForm(ModelForm):
    class Meta:
        model = models.Course
        fields = '__all__'

总结出如何动态生成类
"""


def __new__(cls, *args, **kwargs):
    for field_name in cls.base_fields:
        field = cls.base_fields[field_name]
        attr_dic = {'class': 'form-control'}

        if cls.Meta.form_create is False:
            if field_name in cls.Meta.admin.readonly_fields:
                attr_dic['disabled'] = True
                attr_dic['myattr'] = 'jonathan'
        field.widget.attrs.update(attr_dic)
    return ModelForm.__new__(cls)


def create_dynamic_modelform(model_class, admin_class=None, form_create=False):
    class Meta:
        model = model_class
        fields = "__all__"

    setattr(Meta, 'admin', admin_class)
    setattr(Meta, 'form_create', form_create)

    dynamic_modelform = type("DynamicModelForm", (ModelForm,), {"Meta": Meta, '__new__': __new__})

    return dynamic_modelform
