#!/usr/bin/env python3
# -*-coding:utf-8 -*-
# __author__:Jonathan
# email:nining1314@gmail.com
from django.template import Library
from django.utils.safestring import mark_safe
import os

register = Library()


@register.simple_tag
def get_model_verbose_name(admin_class):
    return admin_class.model._meta.verbose_name

"""
@register.simple_tag
def build_filter_ele(filter_column,admin_class,filter_conditions):

    field_obj = admin_class.model._meta.get_field(filter_column)

    select_ele = "<select class='form-control' name=%s>" % filter_column
    filter_option = filter_conditions.get(filter_column)
    # 1. None 代表没有对这个字段过滤
    # 2. 有值 选中的具体option的val
    if filter_option:
        for choice in field_obj.get_choices():
            if filter_option == str(choice[0]):
                selected = 'selected'
            else:
                selected = ''
            option_ele = "<option value=%s  %s>%s</option>" % (choice[0], selected, choice[1])
            select_ele += option_ele
    else:
        for choice in field_obj.get_choices():
            option_ele = "<option value=%s>%s</option>" % (choice[0], choice[1])
            select_ele += option_ele
    select_ele += "</select>"
    return mark_safe(select_ele)
"""


@register.simple_tag
def build_filter_ele(filter_column, admin_class, filter_conditions):
    """
    目标生成该html网页片段
        <select name="city" lay-verify="required">
            <option value=""></option>
            <option value="0">北京</option>
            <option value="1">上海</option>
            <option value="2">广州</option>
            <option value="3">深圳</option>
            <option value="4">杭州</option>
        </select>
    """

    field_obj = admin_class.model._meta.get_field(filter_column)

    select_ele = "<select name=%s class='form-control'>" % filter_column

    filter_option = filter_conditions.get(filter_column)
    # 1. None 代表没有对这个字段过滤
    # 2. 有值 选中的具体option的val
    if filter_option:
        for choice in field_obj.get_choices():
            if filter_option == str(choice[0]):
                selected = 'selected'
            else:
                selected = ''
            option_ele = "<option value=%s  %s>%s</option>" % (choice[0], selected, choice[1])
            select_ele += option_ele
    else:
        for choice in field_obj.get_choices():
            option_ele = "<option value=%s>%s</option>" % (choice[0], choice[1])
            select_ele += option_ele
    select_ele += "</select>"
    return mark_safe(select_ele)


@register.simple_tag
def build_table_row(row, admin_class):
    """
    1. row queryset库表的一条查询对象
    2. admin_class._display 包含显示的字段
    3. 目标返回 html格式
    <tr>
        <td><a href='#'></a></td>  # 第一个有a标签
        <td></td>
        <td></td>
    </tr>
    4. 查询记录对象 query_obj
    query_obj._meta.get_field('status')  --> <django.db.models.fields.SmallIntegerField:status>
    query_obj._meta.get_field('name')  --> <django.db.models.fields.CharField:name>

    query_obj._meta.get_field('status').choices -->  ((0, '已报名'), (1, '已退费'), (2, '未报名'))
    query_obj._meta.get_field('name').choices -->  []
    小结：灵活输出choices整数值对应的名称  get_status_display()
    """
    row_ele = "<tr><td><input class='row-obj' name='_selected_obj' value='{obj_id}' type='checkbox'></td>".format(obj_id=row.id)
    if admin_class.list_display:
        for index, column_name in enumerate(admin_class.list_display):
            field_obj = row._meta.get_field(column_name)
            if field_obj.choices:
                column_display_func = getattr(row, "get_%s_display" % column_name)
                column_val = column_display_func()
            else:
                column_val = getattr(row, column_name)

            if index == 0:
                td_ele = "<td><a href='{obj_id}/change/'>{column_val}</a></td>".format(obj_id=row.id, column_val=column_val)
            else:
                td_ele = "<td>{column_val}</td>".format(column_val=column_val)
            row_ele += td_ele
    else:
        td_ele = "<td><a href='{obj_id}/change/'>{obj_str}</a></td>".format(obj_id=row.id, obj_str=row)
        row_ele += td_ele
    row_ele += "<td><a type='button' class='btn btn-primary btn-xs' href='{obj_id}/change/'>修改</a> <button type='button' class='btn btn-danger btn-xs'>删除</button><td></tr>".format(obj_id=row.id)
    return mark_safe(row_ele)


@register.simple_tag
def get_selected_m2m_objects(form_obj, field_name):
    """
    1.根据field_name反射出form_obj.instance里的字段对象
    2. 拿到字段对象关联的所有数据
    """

    if form_obj.instance.id:
        field_obj = getattr(form_obj.instance, field_name)
        return field_obj.all()
    else:
        return []


@register.simple_tag
def get_m2m_objects(admin_class, field_name, selected_objs):
    """
    1.根据field_name从admin_class.model反射出字段对象
    2.拿到关联表的所有数据
    3.返回数据
    """
    field_obj = getattr(admin_class.model,field_name)
    all_objects = field_obj.rel.to.objects.all()
    return set(all_objects) - set(selected_objs)


@register.simple_tag
def get_short_description(admin_class, func_name):
    func = getattr(admin_class, func_name)
    if hasattr(func, 'short_description'):
        return getattr(func, 'short_description')
    else:
        return func_name


@register.simple_tag
def get_field_verbose_name(admin_class, column):
    return admin_class.model._meta.get_field(column).verbose_name


@register.simple_tag
def object_delete(obj, recursive=False):
    """
    1. 通过obj._meta.related_objects 拿到关联obj的所有关联对象关系列表
        (<ManyToOneRel: app.paymentrecord>,
        <ManyToOneRel: app.customerfollowup>,
        <OneToOneRel: app.account1>)
    2. 循环关联对象关系表，调用 reverse_lookup_key=i.get_accessor_name() 拿到反向查询的字段名(字符串)，如 'customerfollowup_set'
    3. 反射obj取得所有所有关联对象集合 query_set=getattr(obj, reverse_lookup_key).all()
    4. 所有关联对象集合 query_set元素重复1,2,3步骤，直到没有更深入的关联关系为止

    另外：多对多采用 obj._meta.local_many_to_many
    """
    if not recursive: # 首次调用
        ele = "<ul><li>{object_name}".format(object_name=obj)
    else:
        ele = "<ul>"

    local_m2m = obj._meta.local_many_to_many
    for m2m_field in local_m2m:
        m2m_objs = getattr(obj, m2m_field.name).all()
        for m2m_obj in m2m_objs:
            ele += "<li>{obj_name}:{m2m_name}</li>".format(obj_name=m2m_field.name, m2m_name=m2m_obj)

    for i in obj._meta.related_objects: # step 1
        try:
            reverse_lookup_key = i.get_accessor_name()  # step 2
            query_set = getattr(obj, reverse_lookup_key).all() # step 3
            print('--->', reverse_lookup_key, query_set)
            child_ele = ""
            for o in query_set:
                child_ele += "<li>{model_verbose_name}:<a>{obj_name}</a></li>".format(
                    model_verbose_name=o._meta.verbose_name,
                    obj_name=o)
                if o._meta.related_objects:
                    child_ele += object_delete(o, recursive=True)
            child_ele += ""
            ele += child_ele
        except Exception as e:
            print(e)
    ele += "</ul>"
    return mark_safe(ele)


@register.simple_tag
def get_readonly_field_val(field_name,obj_instance):
    """
    1.根据obj_instance反射出field_name 的值
    :param field_name:
    :param obj_instance:
    :return:
    """
    field_type =  obj_instance._meta.get_field(field_name).get_internal_type()
    if field_type == "ManyToManyField":
        m2m_obj = getattr(obj_instance,field_name)
        return ",".join([ i.__str__() for i in m2m_obj.all()])
    return getattr(obj_instance,field_name)


@register.simple_tag
def get_delete_url(request, nid):
    redirect_url_list = request.path.split('/')
    redirect_url = '/'.join(redirect_url_list[1:4])
    redirect_url = '/' + redirect_url + '/' + str(nid) + '/' + 'delete'+  '/'
    return redirect_url