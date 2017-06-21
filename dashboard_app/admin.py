# -*- coding: utf-8 -*-

from django.contrib import admin
from dashboard_app.models import Widget


class WidgetAdmin( admin.ModelAdmin ):
    prepopulated_fields = {"slug": ("title",)}
    # date_hierarchy = u'create_datetime'
    ordering = [ u'id' ]
    list_display = [ 'title', 'data_contact_email_address' ]
    list_filter = [ 'data_contact_email_address' ]
    search_fields = [ 'title', 'data_contact_email_address' ]
    readonly_fields = [ 'id', 'baseline_value', 'best_value', 'current_value', 'trend_color', 'trend_direction' ]
    radio_fields = { u'best_goal': admin.HORIZONTAL, u'trend_color': admin.HORIZONTAL, u'trend_direction': admin.HORIZONTAL }


admin.site.register( Widget, WidgetAdmin )
