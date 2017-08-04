from django.shortcuts import render, HttpResponse, redirect
from luffyAdmin.admin_base import site
from luffyAdmin import app_config
from utils.page import PageInfo
from django.db.models import Q
from luffyAdmin import forms


print('注册的admin list', site.registered_admins)


def app_index(request):
    return render(request, 'luffyadmin/app_index.html', {'site': site})


def model_table_list(request, app_name, model_name, no_render=False):
    """
    1. 已知跨模块数据site.registered_admins
    2. 根据 app_name, model_name,拿到表对象的admin_class
    3. admin_class.model 就是相应的表对象 --> admin_class.model.objects.filter()
    """
    if model_name in site.registered_admins[app_name]:
        admin_class = site.registered_admins[app_name][model_name]
        if request.method == "POST":  # admin_actoin
            print(request.POST)
            # 获取要执行的函数名
            action_func_name = request.POST.get('admin_action')
            action_func = getattr(admin_class, action_func_name)

            # 获取执行函数参数所需的对象结合
            selected_obj_ids = request.POST.getlist("_selected_obj")
            selected_objs = admin_class.model.objects.filter(id__in=selected_obj_ids)
            action_res = action_func(action_func, request, selected_objs)

            return redirect(request.path)
        else:
            querysets, filter_conditions, page_info,query = get_filter_objs(request, admin_class)

    if no_render: # 被其它函数调用，只返回数据
        return locals()
    else:
        return render(request, 'luffyadmin/model_table_list.html', locals())


def table_obj_change(request, app_name, model_name, object_id, no_render=False):
    """
    from luffyAdmin import forms
    from app import models
    obj = models.Customer.objects.get(id=object_id)
    form = forms.CustomerForm(instance=obj)
    """

    if app_name in site.registered_admins:
        if model_name in site.registered_admins[app_name]:
            admin_class = site.registered_admins[app_name][model_name]
            object = admin_class.model.objects.get(id=object_id)
            form = forms.create_dynamic_modelform(admin_class.model, admin_class=admin_class, form_create=False)
            if request.method == "GET":
                form_obj = form(instance=object)
            elif request.method == "POST":
                form_obj = form(instance=object, data=request.POST)
                if form_obj.is_valid():
                    form_obj.save()

    if no_render:  # 被其它函数调用，只返回数据
        return locals()
    else:
        return render(request, 'luffyadmin/table_object_change.html', locals())


def table_obj_add(request, app_name,model_name, no_render=False):
    print("requestpath", request.path)
    if app_name in site.registered_admins:
        if model_name in site.registered_admins[app_name]:
            admin_class = site.registered_admins[app_name][model_name]

            form = forms.create_dynamic_modelform(admin_class.model, admin_class=admin_class, form_create=True)
            if request.method == "GET":
                form_obj = form()
            elif request.method == "POST":
                form_obj = form(data=request.POST)
                if form_obj.is_valid():
                    form_obj.save()

                    if no_render:
                        redirect_url_list = request.path.split('/')
                        redirect_url = '/'.join(redirect_url_list[1:4])
                        redirect_url = '/' + redirect_url + '/'
                        print(redirect_url)
                        return redirect_url
                    else:
                        return redirect(request.path.rstrip("add/"))

    if no_render:  # 被其它函数调用，只返回数据
        return locals()
    else:
        return render(request, 'luffyadmin/table_object_add.html', locals())


def get_filter_objs(request, admin_class):
    filter_conditions = {}
    query = ""
    for k, v in request.GET.items():
        if k == '_page':
            continue
        if k == '_query':
            query = v
            continue
        if k not in admin_class.list_filter:
            continue
        if v:
            filter_conditions[k] = v

    # 搜索处理模块
    search_fields = admin_class.search_fields
    q1 = Q()
    q1.connector = "OR"
    for field in search_fields:
        para = "%s__icontains" % field
        q1.children.append((para, query))

    # 分页时携带get参数处理
    filter_conditions_str = ""
    for k, v in filter_conditions.items():
        filter_conditions_str += "&%s=%s" % (k, v)
    filter_conditions_str += "&_query=%s" % query

    all_count = admin_class.model.objects.filter(q1, **filter_conditions).count()
    page_info = PageInfo(request.GET.get('_page'), 3, all_count, request.path_info, page_range=7, filter_conditions_str=filter_conditions_str)
    query_sets = admin_class.model.objects.filter(q1, **filter_conditions)[page_info.start():page_info.end()]

    return query_sets, filter_conditions, page_info, query


def table_object_del(request, app_name, model_name, object_id, no_render=False):
    if app_name in site.registered_admins:
        if model_name in site.registered_admins[app_name]:
            admin_class = site.registered_admins[app_name][model_name]
            obj = admin_class.model.objects.filter(id=object_id).first()
            redirect_url_list = request.path.split('/')
            redirect_url = '/'.join(redirect_url_list[1:4])
            redirect_url = '/' + redirect_url + '/'
            print(redirect_url)

            if request.method == "POST":
                obj.delete()
                if no_render:
                    return redirect_url
                else:
                    return redirect(redirect_url)

    if no_render:  # 被其它函数调用，只返回数据
        return locals()
    else:
        return render(request, 'luffyadmin/table_object_delete.html', locals())

