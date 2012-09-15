# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url, include
from mailgun_incoming.views import Incoming

urlpatterns = patterns('',
    url('^incoming/$', Incoming.as_view(), {}, 'mg-incoming'),
)
