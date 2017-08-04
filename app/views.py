from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from app import models
from luffyAdmin import views as admin_views


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Branch
        fields = ('id', 'name',)


@api_view(['GET', 'POST'])
def branch_list(request):
    if request.method == "GET":
        queryset = models.Branch.objects.all()
        serializer = BranchSerializer(queryset, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        print('request', request.data)
        serializer = BranchSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def branch_detail(request, pk):
    try:
        branch_obj = models.Branch.objects.get(pk=pk)
    except models.Branch.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == "GET":
        serializer = BranchSerializer(branch_obj)
        return JsonResponse(serializer.data)

    elif request.method == "PUT":
        print(request)
        data = JSONParser().parse(request)
        serializer = BranchSerializer(branch_obj, data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == "DELETE":
        branch_obj.delete()
        return HttpResponse(status=204)


def customer_list(request):

    app_name = 'app'
    model_name = 'customer'
    view_data = admin_views.model_table_list(request, app_name=app_name, model_name=model_name, no_render=True)
    print("view data", view_data)
    return render(request, 'app/customer/customer_list.html', view_data)


def customer_obj_change(request, app_name, model_name, object_id):
    app_name = 'app'
    model_name = 'customer'
    view_data = admin_views.table_obj_change(request, app_name,model_name,object_id, no_render=True)

    return render(request, 'app/customer/customer_object_change.html', view_data)


def customer_obj_add(request, app_name, model_name):
    app_name = 'app'
    model_name = 'customer'

    if request.method == "POST":
        redirect_url = admin_views.table_obj_add(request, app_name, model_name, no_render=True)
        return redirect(redirect_url)
    else:
        view_data = admin_views.table_obj_add(request, app_name, model_name, no_render=True)
        return render(request, 'app/customer/customer_object_add.html', view_data)


def customer_object_del(request, app_name, model_name, object_id):
    app_name = 'app'
    model_name = 'customer'

    if request.method == "POST":
        redirect_url = admin_views.table_object_del(request, app_name, model_name, object_id, no_render=True)
        return redirect(redirect_url)
    else:
        view_data = admin_views.table_object_del(request, app_name, model_name, object_id, no_render=True)
        return render(request, 'app/customer/customer_object_delete.html', view_data)


def customer_followup_list(request):
    app_name = 'app'
    model_name = 'customerfollowup'
    view_data = admin_views.model_table_list(request, app_name=app_name, model_name=model_name, no_render=True)
    print("view data", view_data)
    return render(request, 'app/customer_followup/customer_followup_list.html', view_data)
