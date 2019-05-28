#!C:\Program Files\Python36 python
# -*- coding: UTF-8 -*-
"""
@author: xiaobai
"""
from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.cart),
    url(r'^add(\d+)_(\d+)/$', views.add),
    url(r'^del_cart/(\d+)/$', views.del_cart),
    url(r'^edit/$', views.edit),
]
