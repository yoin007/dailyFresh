#!C:\Program Files\Python36 python
# -*- coding: UTF-8 -*-
"""
@author: xiaobai
"""


from django.conf.urls import url
from .views import *


urlpatterns = [
    url('^$', index),
    url('^list(\d+)_(\d+)_(\d+)/$', goods_list),
    url(r'^(\d+)/$', detail),
    url(r'^search/', MySearchView()),
]