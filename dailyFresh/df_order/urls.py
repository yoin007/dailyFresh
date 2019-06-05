#!C:\Program Files\Python36 python
# -*- coding: UTF-8 -*-
"""
@author: xiaobai
"""


from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^order_handle/$', views.order_handle),
    url(r'^', views.order),
]
