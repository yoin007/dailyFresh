#!C:\Program Files\Python36 python
# -*- coding: UTF-8 -*-
"""
@author: xiaobai
"""


from django.conf.urls import url
from . import views


urlpatterns = [
    url('^$', views.index),
    url('^list(\d+)_(\d+)_(\d+)/$', views.goods_list),
    url(r'^(\d+)/$', views.detail),
]