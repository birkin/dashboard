# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from dashboard_app import views
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import RedirectView


admin.autodiscover()


urlpatterns = [

    url( r'^admin/', include(admin.site.urls) ),

    url( r'^info/$',  views.info, name='info_url' ),

    url( r'^request_widget/$',  views.request_widget, name='request_widget_url' ),

    url( r'^widgets/$',  views.widgets, name='widgets_url' ),

    url( r'^widget/(?P<identifier>[^/]+)/$',  views.widget, name='widget_url' ),

    url( r'^tag/(?P<tag>[^/]+)/$',  views.tag, name='tag_url' ),

    url( r'^shib_login/$',  views.shib_login, name='shib_login_url' ),
    url( r'^logout/$',  views.shib_logout, name='logout_url' ),

    url( r'^$',  RedirectView.as_view(pattern_name='info_url') ),

    ]
