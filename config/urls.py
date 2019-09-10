from dashboard_app import views
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import RedirectView


admin.autodiscover()


urlpatterns = [

    ## primary app urls...
    url( r'^info/$',  views.info, name='info_url' ),
    url( r'^widgets/$',  views.widgets_redirect, name='widgets_redirect_url' ),
    url( r'^widgets/(?P<identifier>[^/]+)/$',  views.widgets, name='widgets_url' ),
    url( r'^widget_detail/(?P<identifier>[^/]+)/$', views.widget_detail, name='widget_detail_url' ),
    url( r'^request_widget/$', views.request_widget, name='request_widget_url' ),
    url( r'^tag/(?P<tag>[^/]+)/$', views.tag, name='tag_url' ),
    url( r'^admin/', include(admin.site.urls) ),

    ## support urls...
    url( r'^bul_search/$', views.bul_search, name='bul_search_url' ),
    url( r'^login/$', views.login, name='login_url' ),
    url( r'^logout/$', views.shib_logout, name='logout_url' ),

    url( r'^$',  RedirectView.as_view(pattern_name='info_url') ),

    ]
