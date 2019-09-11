# -*- coding: utf-8 -*-

from django.contrib import admin
from dashboard_app.models import Tag, Widget


class TagAdmin( admin.ModelAdmin ):
  list_display = [ 'name', 'slug' ]
  # list_filter = ( 'folder_type', 'parents' )
  ordering = ( 'name', )
  prepopulated_fields = { 'slug': ('name',) }
  # radio_fields = { 'folder_type': admin.VERTICAL }
  # filter_horizontal = ( 'parents', )
  save_on_top = True
  search_fields = [ 'name' ]


class WidgetAdmin( admin.ModelAdmin ):
    prepopulated_fields = {"slug": ("title",)}
    # date_hierarchy = u'create_datetime'
    ordering = [ u'id' ]
    list_display = [ 'title', 'data_contact_email_address' ]
    list_filter = [ 'data_contact_email_address' ]
    search_fields = [ 'title', 'data_contact_email_address' ]
    readonly_fields = [ 'id', 'baseline_value', 'best_value', 'current_value', 'trend_color', 'trend_direction' ]
    radio_fields = { u'best_goal': admin.HORIZONTAL, u'trend_color': admin.HORIZONTAL, u'trend_direction': admin.HORIZONTAL }


admin.site.register( Tag, TagAdmin )
admin.site.register( Widget, WidgetAdmin )
