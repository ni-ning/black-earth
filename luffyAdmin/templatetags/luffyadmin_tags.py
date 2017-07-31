#!/usr/bin/env python3
# -*-coding:utf-8 -*-
# __author__:Jonathan
# email:nining1314@gmail.com
from django.template import Library
from django.utils.safestring import mark_safe

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
    row_ele = "<tr><td><input type='checkbox'></td>"
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
    row_ele += "<td><button type='button' class='btn btn-primary btn-xs'>修改</button> <button type='button' class='btn btn-danger btn-xs'>删除</button><td></tr>"
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