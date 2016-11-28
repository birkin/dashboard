# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf.urls import include, url
from django.contrib import admin


admin.autodiscover()


urlpatterns = [

    url( r'^admin/', include(admin.site.urls) ),

    url( r'^', include('dashboard_app.urls_app', namespace='dashboard') ),  # eg host/callnumber/anything/

    ]
