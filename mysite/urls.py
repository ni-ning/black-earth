from django.conf.urls import url, include
from django.contrib import admin
from mysite import views

urlpatterns = [

    url(r'^$', views.index),
    url(r'^login/$', views.account_login),
    url(r'^admin/', admin.site.urls),
    url(r'^dashboard/$', views.dashboard),
    url(r'^logout/', views.account_logout),
    url(r'^api/', include('app.rest_urls')),
    url(r'^luffyadmin/', include('luffyAdmin.urls')),
    url(r'^app/', include('app.urls')),
    url(r'^test/', views.test)
]
