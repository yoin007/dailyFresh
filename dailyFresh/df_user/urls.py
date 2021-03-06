#!C:\Program Files\Python36 python
# -*- coding: UTF-8 -*-
"""
@author: xiaobai
"""
from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^register/$', views.register),
    url(r'^login/$', views.login),
    url(r'^register_handle/$', views.register_handle),
    url(r'^register_exist/$', views.register_exist),
    url(r'^login_check/$', views.login_check),
    url(r'^info/$', views.info),
    url(r'^site/$', views.site),
    url(r'^order/(\d?)', views.order),
    url(r'^logout/$', views.logout),
]

